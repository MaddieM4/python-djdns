# Provability - Validating your resolution for low-power devices

DJDNS provides excellent validity guarantees - for the server. But since DNS resolution takes place over the original DNS protocol, which has no verification support and is optimized for latency (not security), the server can lie to the client, if the server admin is malicious.

Naturally, as nice as it would be to say "just use a trustworthy server or stand up your own," it would be a lot better to support *proofs* that the client can use to verify the resolution result. The tricky thing is, how can you do this without running a full DJDNS server on the "client" machine? Between page sizes, caching concerns, and the network traffic involved in being a Paxos learner, it's a bit much to ask, especially of low-power devices such as embedded devices, Raspberry PIs, etc., where such resource usage would be a noticeable drag on the performance of the device's primary function.

## Amino

Amino is a TBD protocol that will act as a verifiable data retrieval system, converting "heavy proof" data (such as namecoin or DJDNS resolution) into "light proof" graphs that can be verified trivially on low-power hardware. It replaces the traditional DNS wire format with its own - it is more efficient to send ONLY the proof graph, as the result can be inferred from that, or in more abstract use cases, included as a final step of the proof.

While the Amino wire format is still pre-draft, it is possible to enumerate some principles and practices of how Amino will work.

### Proofs are bigger than just the answer.

This is just common sense, whether in spoken language or in automated environments. As such, we can usually expect the full proof *not* to fit within a UDP packet, which makes life simpler if we just accept the need for TCP. And once we accept that, we find that we have a rather obvious path for building an API - RESTful HTTP!

This means we have a large, existing, optimized ecosystem to build on. For example, it opens the door to caching proofs on disk and using sendfile to ship the results with minimal latency.

### Proofs are directed acyclic graphs, or DAGs.

DAGs sound complicated, but they're not. It's a bunch of objects, connected by one-way arrows, such that there aren't any loops. If you use git, you might be interested to know that every repository you work with stores its history as a DAG.

This is the best way to represent automated proofs, in my opinion. Each element of the proof is either proven, or made relevant, by some previously established dependency, all the way back until you hit commonly-accepted axioms.

DJDNS is a special case of this, where the graph is flat, like a simple git history with no branches. It uses signatures at each step to prove validity, and dependencies to prove relevance, relying on the root page branch-selector list as its axiomatic starting point.

### How does DJDNS resolution serialize to Amino?

From a conceptual/algorithmic point-of-view, DJDNS resolves via alternating phases of find-branch and resolve-from-branch.

 * _find-branch_ - Given an ordered list of branch selectors (regexes), find the first match.
 * _resolve-from-branch_ - Given a branch's contents, either recurse to another page (branch list), or return records.

These are exactly the distinct steps we can represent and validate concisely with Amino. Each page's worth of recursion is expressed as two proof elements, one for the branch list, the other for the branch contents.

An example proof, in pseudocode:

1. The branch selectors of the root page are [...]. *Client uses signatures to validate that this is true.*
2. The contents of the matching branch are {...}. *Client uses signatures for validation, and can use the information in step 1 to test for itself that this is the first regex match.*
3. Now we go to page "..." with branch selector list [...]. *Sig validation, uses branch contents from step 2 to confirm this is the right action.*
4. The contents of the matching branch are {...}. *Works just like step 2.*
5. Continue recursing through pages until...
6. Matching branch contents are {...}. *Client can confirm that branch contains records, and can evaluate and serve them via Pymads, as it would be served by a real DJDNS server.*

So it's just a matter of building a daemon that serves DNS, and acts as an HTTP client to retrieve proofs from DJDNS/Amino servers. When it gets a DNS request, it downloads and parses a proof, and serves the answer back to the DNS client.

### Other flavors of Amino

...are not really a priority for me right now. However, it should easily support DJDNS, general DNS proofs (confirm that multiple signing servers agree), and many non-DNS use cases. I have not put a lot of thought yet into an optimized proof structure for Namecoin - that's an exercise I'm leaving to CJD.

My only goal here is to have a format that's flexible and modular enough to support any proof system in a self-describing DOCTYPE-ish way, as long as the proof can be expressed as a DAG of proof elements (which each have a bytestring content and optionally blank signature list).
