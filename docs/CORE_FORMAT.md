# Core format of DJDNS registry data

Each registry page is a JSON-serializable object {}, containing a mandatory branch list, and optionally, a metadata object.

```json
{
    "meta": {
        ...
    },
    "branches": [
        ...
    ]
}
```

## Metadata

The metadata object's properties are all optional, but the following are typical:

 * _authority_ - string describing who is responsible for administrating the page.
 * _contact_ - instructions on how to get in touch with page _authority_.
 * _about_ - short description of page.
 * _policy_ - recommendations and requirements for submitting change proposals.

```json
{
    "meta": {
        "authority": "https://github.com/campadrenalin/djdns-hype-flat/issues/12",
        "contact": "Liam on HypeIRC, or @campadrenalin on Github",
        "about": "Liam's DJDNS page for the Riddims music streaming service.",
        "policy": "Private"
    },
    "branches": [
        ...
    ]
```

## Branch list

Ordered list of branches, which are tested in-order during regex-based search (see RESOLUTION.md).

```json
{
    "meta": {
        ...
    },
    "branches": [
        { branch data },
        { branch data },
        { branch data },
        ...
        { branch data }
    ]
}
```

## Branch

Each branch contains three mandatory properties.

 * _selector_ - regex string for traversal
 * _targets_ - list of URLs to redirect to.
 * _records_ - list of DNS records.

During resolution, if a branch matches, the server first checks to see if there are any records available in the branch - if so, immediately return those. If not, go through the targets in order, attempting to retrieve a result set from each, and return the first non-empty result set (counting errors as an empty result set).

Each target's behavior depends on the protocol component of the URL.

 * file://some/file/on/disk.json - locally available page file. This is default, so usually the file:// is omitted for clarity. Relative addresses are relative to a configurable root directory.
 * dns://8.8.8.8/ - Ask another server via DNS protocol.
 * DEJE distribute registry - _schema to be determined._

```
{
    "selector": "(.*\\.|^)example\\.com$",
    "targets": [],
    "records": [
        { record data },
        { record data },
        ...
        { record data }
    ]
}

OR...

{
    "selector": "(.*\\.|^)example\\.com$",
    "targets": [
        "private/example.json",
        "dns://122.68.91.32/"
    ],
    "records": []
}
```

## Record format

Each record contains:

 * _rtype_ - Record type, default "A"
 * _rclass_ - Record class, default "AAAA"
 * _rdata_ - Record contents, in an unpacked/readable form (see [Pymads][pymads] for reference, but mostly should be straightforward/obvious)
 * *domain_name* - Selectors are usually very regex-y, and crap at representing the actual domain name of the record. This allows you to override that. It's also useful when you're providing records for multiple different domain names in a single result set.

# The future

This specification is only going to grow over time, as features are added. DJDNS is designed to be forward-compatible with convention-based extensions and specialized features. See EXTENSIBILITY.md for more information.

[pymads]: https://github.com/campadrenalin/pymads
