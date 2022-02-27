Taranvir Singh ts903

I made the recursive client by establishing a connection to root DNS server like required.
Once a hostname was not in the root DNS table, I got the address from top level DNS server.
I created this connection, and then for each request onward I consulted the root server, and 
if hostname was not in the root servers' DNS table, I checked the top level server
which then searched its own table.

There are no issues with the code.

The main issue I faced was figuring out how to implement the client algorithm and write my code using recusive lookup algorithm.

This is whole project was a learning experience. I did not know almost anything before starting and learned so much by the end.