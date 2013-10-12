# Extending the DJDNS registry for fun and profit

There are three big rules to parsing DJDNS pages:

1. Ignore what you aren't familiar with.
2. Don't drop unfamiliar data during modifications, copies, dumps, signatures...
3. It's just JSON!

Between these three rules, as long as you otherwise follow the specification laid out in CORE_FORMAT.md, you can have all the extra crap you want in your registry pages. Servers that don't understand your extensions will simply ignore them, or in reproduction/signature scenarios, preserve that data verbatim.

This lays out an ideal environment for establishing standard extensions by popular convention, such that they can be adopted into the core formal standard after proving themselves in the wild.

## Implemented extensions

 * User registry. See IDENTITY_REGISTRATION.md.

## Planned extensions

There are actually a few extensions that I'm planning to establish myself.

### Reverse DNS

RDNS is not built into the current registry format. This should be pretty easy to handle by using a variant of [traditional reverse lookup](https://en.wikipedia.org/wiki/Reverse_DNS_lookup) using PTR records and the neutral \*.rdns TLD (which can then bounce to a top-level RDNS page, which bounces to separate IPv4 and IPv6 pages, and further breaking down by IP until landing on private pages that may or may not be RDNS-specific).

### Bitcoin addresses

For security reasons, it's not a bad idea at all to have your Bitcoin addresses (personal or site-level) in the DJDNS registry. This provides a universal place to look up when you want to send money to an email address - which means we also want to support large-scale online wallet managers, where it makes more sense to point to an API endpoint than to include individual addresses in the DJDNS registry.

A bitcoin address is expressed as an object as follows:

```json
{
    "address": "...",
    "signature": { signature object }
}
```

Using the TBD EJTP signature format (is a signature of the whole bitcoin object structure, minus "signature" key/value pair).

### Site-level

List of addresses is included in branch under key "bitcoin".

```json
{
    "selector" : "some_regex",
    "targets": [],
    "records": [...],
    "bitcoin": [
        {
            "address": "...",
            "signature": {...}
        }
    ]
}
```

### User-level

Included as an arbitrary extension to an EJTP identity in a site's users list (identity format also supports arbitrary extension data).

```json
{
    "selector" : "some_regex",
    "targets": [],
    "records": [...],
    "users": {
        "<serialized ident.location>" : {
            "name": "mordecai@lackadaisy.com",
            "location": [...],
            "encryptor": [...],
            "bitcoin": [
                {
                    "address": "...",
                    "signature": {...}
                }
            ]
        }
    }
}
```

### API endpoint

I don't feel like standardizing an API, so I'm directing convention on how to list API endpoints (including expected request/response format). That way behavior can be directed by recognizing the contents of the "standard" property.

Not sure there's a point to supporting this at user-level, but honestly, why not.

```json
{
    "selector" : "some_regex",
    "targets": [],
    "records": [...],
    "bitcoin_api": [
        {
            "standard": "http://some.url/that/describes/standard",
            "endpoint": "https://actual.url/for/api/endpoint"
        }
    ]
}
```

## In conclusion

Your only limit to extending the registry format is that it has to be valid JSON. Oh, and it can't conflict with the accepted core standard. So two limits, but is that really so bad? No, you can do amazing things, and you should.

Keep in mind that bloated branch size can be bad for efficiency when you want to provide provability as per PROVABILITY.md.
