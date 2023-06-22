# REST API

GET - /api/posts zwraca wszystkie posty\
GET - /api/posts?limit=5 zwraca 5 ostatnich postów \
GET - /api/posts?limit=5&offset=5 zwraca 5 postów omijając 5 pierwszych \
GET - /api/posts?author=author zwraca posty wybranego autora\
GET - /api/posts/id zwraca wybrany post

POST - /api/posts
>{\
&emsp;"author": string,\
&emsp;"photo": url,\
&emsp;"title": string,\
&emsp;"subtitle": string,\
&emsp;"text": html\
}