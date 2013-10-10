# How does DJDNS resolve a request?

The DJDNS registry is broken up into *pages.* Each page has a list of *branches* in it.

Each branch has:

 * A match regex, called a *selector*
 * A list of *targets* - pages to jump to (like hyperlinks). Ignored if records are available (avoids recursion).
 * A list of *records* - actual records to return.

So to resolve a hostname like "example.com", you start at the "root page", and go down each of its branches until you find one that matches.

The following diagram is simplified in some ways - the regexes and page addresses are not technically accurate, for example. However, it's a decent illustration of the actual recursive resolution mechanism, and the "diskdemo" directory in this repository gives a detailed example of how such a registry is set up.

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
  |                     |<-|
  | ... some branches   |
  |                     |
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

See CORE_FORMAT.md for more information about the structure/storage format in detail.
