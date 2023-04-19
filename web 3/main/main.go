package main

import (
	"context"
	"fmt"
	"log"
	"math/big"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
)

func main() {
	// Connect to the local Ganache network using an Ethereum client
	client, err := ethclient.Dial("http://127.0.0.1:7545")
	if err != nil {
		log.Fatal(err)
	}

	// Get the address of the smart contract you want to interact with
	contractAddress := common.HexToAddress("0x290c8930a0Fc7F4631Ca32196615552fE147140B")

	// Create a new instance of the smart contract using the contract address and the Ethereum client
	instance, err := NewMyContract(contractAddress, client)
	if err != nil {
		log.Fatal(err)
	}

	// Set up a transaction signer to sign Ethereum transactions
	privateKey := "0x7a028b69496c92848d2874ca606a1c517138ea7ef933241ad6327525d2643fad"
	privateKeyECDSA, err := crypto.HexToECDSA(privateKey)
	if err != nil {
		log.Fatal(err)
	}
	auth := bind.NewKeyedTransactor(privateKeyECDSA)

	// Call a function on the smart contract
	greeting, err := instance.GetGreeting(&bind.CallOpts{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Greeting:", greeting)

	// Send a transaction to update the smart contract state
	newGreeting := "Hello, world!"
	tx, err := instance.SetGreeting(auth, newGreeting)
	if err != nil {
		log.Fatal(err)
	}

	// Wait for the transaction to be confirmed on the blockchain
	ctx := context.Background()
	receipt, err := bind.WaitMined(ctx, client, tx)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Transaction hash:", receipt.TxHash.Hex())
}
