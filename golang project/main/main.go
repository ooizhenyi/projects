// test using https://scrapeme.live/shop/

package main

import (
	"bufio"
	// "bytes"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"
	"net/http"
	"github.com/gocolly/colly/v2"
	"github.com/sclevine/agouti"
)

// Define a struct to hold product data
type Product struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Price       string `json:"price"`
	ImageURL    string `json:"image_url"`
}

// Determine if the URL points to a dynamic website
func isDynamic(url string) bool {

	    // Create an HTTP client
		client := &http.Client{}

		// Create an HTTP request
		req, _ := http.NewRequest("GET", url, nil)

	
		// Make the request
		resp, _ := client.Do(req)

		defer resp.Body.Close()
	
		// Check if the response headers contain "Content-Length" and "ETag"
		if resp.Header.Get("Content-Length") != "" && resp.Header.Get("ETag") != "" {
			fmt.Println("This is a static page")
			return false
		} else {
			fmt.Println("This is a dynamic page")
			return true
		}
}

func scrapeWithSelenium(url string) ([]Product, error) {
    // Start a new WebDriver session with a headless Chrome browser
    driver := agouti.ChromeDriver(agouti.ChromeOptions("args", []string{"--headless", "--disable-gpu"}))
    err := driver.Start()
    if err != nil {
        return nil, err
    }
    defer driver.Stop()

    // Navigate to the target URL
    page, err := driver.NewPage(agouti.Browser("chrome"))
    if err != nil {
        return nil, err
    }
    err = page.Navigate(url)
    if err != nil {
        return nil, err
    }

    // Wait for the page to fully load
    err = page.Session().SetImplicitWait(5000)
    if err != nil {
        return nil, err
    }

    // Extract the product data from the page
    products := make([]Product, 0)

    productCards := page.All("li.product")
	numProducts, err := productCards.Count()
	if err != nil {
		fmt.Printf("numProducts %d",numProducts)
		return nil, err

	}
    for i := 0; i < numProducts; i++ {
        productCard := productCards.At(i)
        product := Product{}
        product.Name, _ = productCard.Find("h2").Text()
        // product.Description, _ = productCard.Find(".product-description").Text()
        product.Price, _ = productCard.Find(".price").Text()
        product.ImageURL, _ = productCard.Find("img").Attribute("src")
        products = append(products, product)
    }

    return products, nil
}


func main() {
	// Get the URL from the user input
	fmt.Print("Enter the URL to scrape: ")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	url := scanner.Text()

	// Check if the URL is dynamic or not
	if isDynamic(url) {
		fmt.Println("is dynamic")
		// Use Selenium to scrape the dynamic website
		products, err := scrapeWithSelenium(url)
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		// Generate the JSON file only if there are products
		if len(products) > 0 {
			// Marshal the slice of products to JSON
			jsonData, err := json.MarshalIndent(products, "", "  ")
			if err != nil {
				fmt.Println("Error:", err)
				return
			}

			// Write the JSON data to a file
			err = os.WriteFile("products.json", jsonData, 0644)
			if err != nil {
				fmt.Println("Error:", err)
				return
			}

			fmt.Println("Scraped data saved to products.json")
		} else {
			fmt.Println("No products found, not generating JSON file.")
		}
	} else {
		fmt.Println("is static")
		// Use Colly to scrape the static website
		// Create a new Colly collector
		c := colly.NewCollector(
			// Set the maximum depth to 2 to avoid scraping too many pages
			colly.MaxDepth(2),
		)

		// Set rate limiting to avoid getting banned by the website
		c.Limit(&colly.LimitRule{
			DomainGlob:  "*",
			Parallelism: 2,
			Delay:       2 * time.Second,
		})

		//Define a slice to hold the scraped products
		products := make([]Product, 0)

		// Define the function to be executed when visiting each product page
		c.OnHTML("li.product", func(e *colly.HTMLElement) {
			// Create a new Product struct
			product := Product{}

			// Extract the product name
			product.Name = e.ChildText("h2")

			// Extract the product description
			// product.Description = e.ChildText(".product-description")

			// Extract the product price
			product.Price = strings.TrimSpace(e.ChildText(".price"))

			// Extract the product image URL
			product.ImageURL = e.ChildAttr("img", "src")

			// Add the product to the slice of products
			products = append(products, product)

			// Print the product data
			fmt.Printf("Product Name: %s\n", product.Name)
			// fmt.Printf("Product Description: %s\n", product.Description)
			fmt.Printf("Product Price: %s\n", product.Price)
			fmt.Printf("Product Image URL: %s\n", product.ImageURL)
		})
		
		// Start the scraping process
		c.Visit(url)

		// Generate the JSON file only if there are products
		if len(products) > 0 {
			// Marshal the slice of products to JSON
			jsonData, err := json.MarshalIndent(products, "", "  ")
			if err != nil {
				fmt.Println("Error:", err)
				return
			}

			// Write the JSON data to a file
			err = os.WriteFile("products.json", jsonData, 0644)
			if err != nil {
				fmt.Println("Error:", err)
				return
			}

			fmt.Println("Scraped data saved to products.json")
		} else {
			fmt.Println("No products found, not generating JSON file.")
		}
	}
}


		
