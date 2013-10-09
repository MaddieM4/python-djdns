# How does DJDNS resolve a request?

The DJDNS registry is broken up into *pages.* Each page has a list of *branches* in it.

Each branch has:

 * A match regex, called a *selector*
 * A list of *targets* - pages to jump to.
 * A list of *records* - actual records to return.

So to resolve a hostname like "example.com", you start at the "root page", and go down each of its branches until you find one that matches.

```

  ------ ROOT PAGE ------
  |                     |
  |                     |
  | --- branch 1 ------ |
  | |                 | |
  | | "*.org"         | | "example.com" does not match regex "*.org"
  | | ["/tld/org/"]   | |
  | | []              | |
  | ------------------- |
  |                     |
  |                     |
  | --- branch 2 ------ |
  | |                 | |
  | | "override.com"  | | "example.com" does not match regex "override.com"
  | | []              | |
  | | [{record data}] | |
  | ------------------- |
  |                     |
  |                     |
  | --- branch 3 ------ |
  | |                 | |
  | | "*.com"         | | "example.com" matches regex "*.com"!
  | | ["/tld/com/"]   | | Continue lookup at the top of the "/tld/com/" page.
  | | []              | |  |
  | ------------------- |  |
  |                     |  |
  |                     |  |
  -----------------------  |
                           |
  ------ /tld/com/ ------  |
  |                     |  |
  | ... some branches   |  |
  |                     |<-|
  | --- branch N ------ |
  | |                 | |
  | | "example.com"   | | Found a regex match for "example.com"!
  | | []              | | No targets, so we don't jump to another page.
  | | [{record data}] | | Contains a record we can return to the client!
  | ------------------- |
  |                     |
  | ... other branches  |
  |                     |
  -----------------------
```

For a server, most of this information will be cached, but the server will download pages as necessary to fulfill a request.

## Record data format

Each record contains:

 * An optional record "type", assumed "A"
 * An optional record "class", assumed "IN"
 * Mandatory "rdata", for record contents
 * Provide-it-if-you-know-what's-good-for-ya "hostname", which will usually be different from regex.

This probably deserves to be in its own section on DJDNS registry format.
