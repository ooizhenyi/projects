package main

import (
	"bufio"
	"fmt"
	"os"
	"time"

	"github.com/gocolly/colly/v2"
)

func main() {
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

	// Define the function to be executed when visiting each page
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		// Print the URL of the current page
		fmt.Println("Scraping: ", e.Request.URL.String())
		// Print the value of the href attribute of each link
		fmt.Println("Link: ", e.Attr("href"))
		// Visit the link found on the current page
		e.Request.Visit(e.Attr("href"))
	})

	// Define the function to be executed when a page request is completed
	c.OnResponse(func(r *colly.Response) {
		// Check the status code of the response
		if r.StatusCode != 200 {
			// Handle errors, such as 404 or 500 errors
			fmt.Println("Error:", r.StatusCode)
		}
	})

	// Get the URL from the user input
	fmt.Print("Enter the URL to scrape: ")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	url := scanner.Text()

	// Visit the URL using the Visit() method
	c.Visit(url)
}
