# User registry

It is not enough that a site alone be listed in the registry - no, we want to host EJTP identities there, too! Hot ones, cold ones, host all the identities. The idea is that an identity cache (expressed as a JSON object {}), according to EJTP standard format, can just be dropped into a branch as a "users" property, as a sibling to "selector", "targets", and "records".

Of course, these users are only accessible if you reach the branch while traversing based on the user's hostname. For example, when the server looks for "joe@example.com", it will first look up "example.com" as if for a regular old record set, find the user data, and return the name matches for "joe@example.com" (there may be more than one, as identities are considered unique by location). So if you store that data in the wrong place, the traversal will not find it, because *duh.*

```json
{
    "selector" : "some_regex",
    "targets": [],
    "records": [...],
    "users": {
        "[\"local\",null,\"tom\"]": {
            "name": "tom@example.org",
            "location": ["local", null, "tom"],
            "encryptor": ["rotate", 5]
        },
    }
}
```

## How to add your own identities

1. Make an EJTP Identity (leaving this as an exercise to the reader, until I have the fancy new interactive Identity creator working).
2. Make sure you have a private page for your domain(s).
3. Make sure the name is in email-address form, like "mike@rowe.net", where the domain is a domain in your DJDNS private page.
4. Embed the identity cache in your domain's branch.

Once your Identity is in the registry, people will be able to access it from any public API endpoint over HTTP, like this:

http://mesh.roaming-initiative.com/idents/philip@ri.hype

This is a temporary API that doesn't even have SSL. It will be replaced with something better, because let's face it, it kinda has to be. But it should be enough (for now) to do its immediate job - bootstrapping the decentralized version of the registry.
