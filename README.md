# python-djdns

This is a DJDNS server written in Python. It is a Decentralized DNS server for a more secure, free internet.

## Decentralized DNS is cool.

Which is why I'm building a version on top of the DEJE library. The DEJE platform provides security,
authentication, democratic management, and psychotic levels of cacheability.

## How resistant is this system to tampering?

Djdns is based on a hierarchy of MCP pages. Each can store references to subpages, which represent subdomains.
Each page is publicly readable, but only a defined set of participants can write to it, and even then, they
have to have group consensus. Like any MCP page, participant set changes are Track 2 operations, and for this
type of page, domain modifications are Track 1. Depending on the page settings, it'll usually take a consensus
of about 70% of participants to add or remove another participant, but only a little over 30% to modify domain
information.

The system is cryptographically secure such that you can verify the entire chain of operations given a known
accurate previous state. If someone tries to send you false information, your ctdns implementation will not
only notice that you're being lied to, but start trying alternate sources of information to find a truthful one.
Only participants can edit the participant set or the domain information, and it requires group consensus in the
amounts dictated above.

### What about Sybil attacks? What is the policy for new domains?

The problem summarrized in this question is one that most decentralized DNS implementations struggle with. What
is the "price" of a domain registration? In namecoin, it's a bitcoin value, so money basically. With the more
loose web-of-trust approaches, registry space truly is infinite since the system doesn't concern itself with
name collisions except to pick the most personally algorithmically trusted contender in the collision. Some systems
propose rate limiting, but this is very easy to defeat with Sybil attacks - a strategy named after a famous
psychiatric case study of a woman with multiple personality disorder, in which the attacker uses a multitude of
distinct personas (stolen, or generated mechanically or by hand) to defeat "one per customer" sorta limits.

Djdns takes an entirely different approach that I like to call recursive democracy, which averts such problems 
altogether, by not establishing a "global policy" per se at all, except in the most fundamentally basic and
democratic terms. As stated earlier in the readme, every page represents a subdomain (except the TLD page, if you
want to be technical and pedantic about it). You can think of the write-enabled participants as moderators for that
page, in a mass-moderation scenario. Without group agreement, a change of any kind will fail. This system can easily
support hundreds of thousands of "moderators", especially thanks to the Digitally Distributed Democracy vote
augmentation system that lets you declare yourself to be abstaining from voting, and donating your "vote power" to
another party (or parties, based on percentages) while you're "offline for voting".

So, basically, if you want a domain, the price is to get the moderators of a subdomain page to approve and add your
information to the page. Whatever their requirements are, are the requirements to get that domain (though it could be
as small and simple as just asking). In the event of mass adoption, you'll have these x.y.z.something.or.other crazy
long subdomains managed by just a few people, which are easy to obtain; and top-level domains, which require community
approval and momentum on a massive scale, and thus will be much better-vetted and more valuable. And every subdomain
page is invite-only for write permissions.

## And there's no name collisions... ever?

Right. It's not like WOT, where it will try to guess the best known option based on who you personally trust. It's a
community-managed ecosystem with fine-grained syncronization controls and configurability. Everybody's on the
"same page", so to speak, only storing and managing the parts they have interest in. The worst you can possibly do
is get an out-of-date copy, which will store enough participant references that you can ask around and make sure you
have the most recent copy.

## Is this a high-bandwidth thing?

Nope. It's also, in theory, pretty fast, thanks to its push-based design and UDP transport, and only transferring
control data and deltas. It's a little bit like git-based DNS.

Not only that, but you get to cache a lot. And I mean, a LOT. In the early versions of ctdns, before it becomes too
big to be practical anymore except for intentionally participating servers, when you want to resolve (say)
"brickwindows.ff.ct", you will download and store the entire table of top level domains, the entire table of .ct
domains, and the entire table of .ff.ct domains. But once you have that stuff, you can just keep it up to date quite
passively, and not have to do any sort of DNS query at all to the internet to resolve *.ff.ct or *.ct domains. If
you've noticed that this completely prepares you for the censorship apocalypse scenario where the government blocks
or DDoS's every single source of domain information, you get a jammy dodger.

The secret is that djdns sets up as an MCP node for the internet at large (P2P, distributed protocol over UDP and
other transports), and as a DNS server on localhost. So you configure your computer to use itself as a nameserver,
et voila, it will accept regular old DNS requests, do any MCP requests/downloading necessary (usually none, after 
"warming up"), and return the resolved name just like that. All your existing technology will *just work.*

## Are there any downsides?

Well, only one big one. You may have picked up on a design intention: the more people who have vote priveleges, the
more resistant to change a page is, because it needs more people to agree. This works very well for preventing
destructive or disruptive changes from poisoning the system, but also inhibits reaction time in the event of a service
moving to a different IP address, or being hacked by Estonians. There may be serious delays for top-level pages to
catch up to reality.

## How close is this to completion?

Hard to say, I've only just started it (though I have some very strong design ideas, so it's more a matter of implementing
those and filling in the gaps than figuring it all out as I go). Quite a bit of the work will be handled "invisibly" by
the DEJE library project, and most of the remainder is setting up the DNS server face of it, and the page
structure specifics.

So basically, I have no idea, and refuse to make any sort of promises about deadlines, until I'm quite confident in my
ability to acheive them without running into unexpected complications.

## Is this anything like CJDNS?

No, and the confusion is mostly on the part of CJD for naming his really cool software in a really misleading way. CJDNS
stands for CJD's Networking Suite, and doesn't do DNS at all. Djdns stands for DEJE DNS, and DNS is all it does.
You can think of it as *CJD NS* vs *DJ DNS*.
