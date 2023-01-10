package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"

	//"golang.org/x/crypto/acme/autocert"
	//"crypto/tls"
)

// defining global variables
var lhcert_path string = "TLS/localhost.pem"
var lhkey_path string = "TLS/localhost-key.pem"

func showhome(w http.ResponseWriter, r *http.Request) {

	switch r.Method {
	case http.MethodGet:
		w.Header().Set("Content-Type", "text/plain")
		w.Write([]byte("testserver"))
	case http.MethodPost:
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}
		log.Println(string(body))
	}
}

func showline(w http.ResponseWriter, r *http.Request) {

	switch r.Method {
	case http.MethodGet:
		w.Header().Set("Content-Type", "text/plain")
		w.Write([]byte("hello stanman, how you been, what do you need?"))
	case http.MethodPost:
		body, err := ioutil.ReadAll(r.Body)
		transfer_package := string(body)
		if err != nil {
			panic(err)
		}
		log.Println(transfer_package)
		createtext(transfer_package)
		emailprotocol()
	}
}

func emailprotocol() {
	courier := exec.Command("python", "sheetswriter.py")
	if err := courier.Run(); err != nil {
		fmt.Println(err)
	}
}

func createtext(text string) {
	textfile, err := os.Create("incoming.txt")
	textfile.WriteString(text)
	if err != nil {
		fmt.Println(err)
		textfile.Close()
		return
	}
	
}

func main() {
	fmt.Println("server running and listening on 443")
	http.HandleFunc("/postings", showline)
	http.HandleFunc("/", showhome)
	err := http.ListenAndServeTLS(":8443", lhcert_path, lhkey_path, nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }

}

