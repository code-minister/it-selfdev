package main

import (
	"html/template"
	"log"
	"math/rand"
	"net/http"
	"os"
	"os/exec"
)

var images = []string{
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F0.gif?alt=media&token=0fff4b31-b3d8-44fb-be39-723f040e57fb",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F1.gif?alt=media&token=2328c855-572f-4a10-af8c-23a6e1db574c",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F10.gif?alt=media&token=647fd422-c8d1-4879-af3e-fea695da79b2",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F11.gif?alt=media&token=900cce1f-55c0-4e02-80c6-ee587d1e9b6e",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F2.gif?alt=media&token=8a108bd4-8dfc-4dbc-9b8c-0db0e626f65b",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F3.gif?alt=media&token=4e270d85-0be3-4048-99bd-696ece8070ea",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F4.gif?alt=media&token=e7daf297-e615-4dfc-aa19-bee959204774",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F5.gif?alt=media&token=a8e472e6-94da-45f9-aab8-d51ec499e5ed",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F7.gif?alt=media&token=9e449089-9f94-4002-a92a-3e44c6bd18a9",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F8.gif?alt=media&token=80a48714-7aaa-45fa-a36b-a7653dc3292b",
	"https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F9.gif?alt=media&token=a57a1c71-a8af-4170-8fee-bfe11809f0b3",
}

type PageData struct {
	Url     string
	Figlet  string
	Fortune string
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	// Вызываем утилиты Linux
	figletOut, _ := exec.Command("/usr/bin/figlet", "MEOW!").Output()
	fortuneOut, _ := exec.Command("/usr/games/fortune").Output()

	// Выбираем случайную ссылку
	url := images[rand.Intn(len(images))]

	data := PageData{
		Url:     url,
		Figlet:  string(figletOut),
		Fortune: string(fortuneOut),
	}

	htmlTemplate := `
	<html>
	  <head>
		<style type="text/css">
		  body {
			background: black;
			color: white;
		  }
		  div.container {
			max-width: 500px;
			margin: 50px auto;
			border: 20px solid white;
			padding: 10px;
			text-align: center;
		  }
		  h4 {
			text-transform: uppercase;
		  }
		  pre.ascii {
			color: #00ffcc;
			font-weight: bold;
		  }
		  div.quote {
			margin-top: 20px;
			color: #aaaaaa;
			font-style: italic;
		  }
		  a { color: #66ccff; }
		</style>
	  </head>
	  <body>
		<div class="container">
		  <pre class="ascii">{{.Figlet}}</pre>
		  <h4>Cat Gif of the day</h4>
		  <img src="{{.Url}}" style="max-width: 100%;" />
		  <div class="quote">{{.Fortune}}</div>
		  <p><small>Courtesy: <a href="http://www.buzzfeed.com/copyranter/the-best-cat-gif-post-in-the-history-of-cat-gifs">Buzzfeed</a></small></p>
		</div>
	  </body>
	</html>
	`

	t, _ := template.New("index").Parse(htmlTemplate)
	t.Execute(w, data)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "5000"
	}

	http.HandleFunc("/", indexHandler)
	log.Printf("Сервер запущен на http://localhost:%s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}