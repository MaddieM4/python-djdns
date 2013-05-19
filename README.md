# python-DJDNS

This is a DJDNS server written in Python. It is a Decentralized DNS server for a more secure, free internet.

# Proof-of-concept Install Guide

Right now none of the P2P magic works or is used, due to the so-called "bootstrapping issue" in DEJE.All the data is fed from on-disk files that would normally be hosted in DEJE. The positive side is that you can try out DJDNS in its current demo state without installing a bunch of extra crap.

In these instructions, we're going to build and install everything in a virtualenv, so that nothing touches the system state, and cleaning up is as simple as deleting the 'djdns' virtualenv folder afterwards. Keep in mind that I have no idea how you would install this on Windows, this is all UNIX-y command line stuff and assumes you have git and python-virtualenv installed.

```bash
$ virtualenv djdns
$ cd djdns
$ source ./bin/activate
$ git clone https://github.com/campadrenalin/pymads
$ git clone https://github.com/campadrenalin/python-djdns
$ cd pymads
$ python setup.py install
$ cd ../python-djdns
$ python setup.py install
$ python -m djdns.server # Run the server
```

Now, in another terminal or tab or whatever, you should be able to hit that running server with DNS requests using the program 'dig' (you may need to install the dnsutils package).

```bash
$ dig @localhost -p 8989 in.root.demo       # 1.2.3.4
$ dig @localhost -p 8989 in.subbranch.demo  # 5.5.5.5
$ dig @localhost -p 8989 in.b3.demo         # 5.6.7.8
```

Feel free to explore the diskdemo directory and play with its contents, to see how the traversable structure of DJDNS works. For further reference on the specification, see [this Github comment](https://github.com/campadrenalin/python-djdns/issues/2#issuecomment-18111938).

# About DJDNS

## Decentralized DNS is cool.

Which is why I'm building a version on top of the DEJE library. The DEJE platform provides security,
authentication, democratic management, and psychotic levels of cacheability.

## How resistant is this system to tampering?

DJDNS is based on a hierarchy of DEJE documents. Each can store references to other documents, based on regexes.
For example, "You can find out about all \*.hype domains over here in this other place." Each page can hold
arbitrary data, so that DJDNS will be forward-compatible, but a few types of data will be understood in very
early versions: domain resolution information, domain ownership information (WHOIS), and EJTP identities. After
that, it'll probably be used to replace the existing certificate system used by SSL, but that's down the road
aways.

The system is cryptographically secure such that you can verify the entire chain of operations given a known
accurate previous state. If someone tries to send you false information, your DJDNS implementation will not
only notice that you're being lied to, but start trying alternate sources of information to find a truthful one.
Control over who can edit a document is fully customizable, and designed to strike an ideal balance between
permissive areas and privately controlled areas, and between automation and personal approval.

### What about Sybil attacks? What is the policy for new domains?

The problem summarrized in this question is one that most decentralized DNS implementations struggle with. What
is the "price" of a domain registration? In namecoin, it's a bitcoin value, so money basically. With the more
loose web-of-trust approaches, registry space truly is infinite since the system doesn't concern itself with
name collisions except to pick the most personally algorithmically trusted contender in the collision. Some systems
propose rate limiting, but this is very easy to defeat with Sybil attacks - a strategy named after a famous
psychiatric case study of a woman with multiple personality disorder, in which the attacker uses a multitude of
distinct personas (stolen, or generated mechanically or by hand) to defeat "one per customer" sorta limits.

DJDNS takes an entirely different approach that I like to call recursive democracy, which averts such problems 
altogether, by not establishing a "global policy" per se at all, except in the most fundamentally basic and
democratic terms. As stated earlier in the readme, every page represents a subdomain (except the TLD page, if you
want to be technical and pedantic about it). Each page can have any kind of custom rules for moderation and
modification of its contents. The TLD can be administrated by a voting consensus of hundreds of thousands of
people. Your site page can be administrated by your web dude.

Some pages will use automatic approval (domain follows specific rules and isn't taken? Add it to the list!),
others will use manual (must be approved by some critical mass of moderators), some will use a combination.
The price of a domain is just convincing a system or group of people to point a delegation regex to your
DJDNS document.

## And there's no name collisions... ever?

Right. It's not like WOT, where it will try to guess the best known option based on who you personally trust. It's a
community-managed ecosystem with fine-grained syncronization controls and configurability. Everybody's on the
"same page", so to speak, only storing and managing the parts they have interest in. The worst you can possibly do
is get an out-of-date copy, which will store enough participant references that you can ask around and make sure you
have the most recent copy.

## Is this a high-bandwidth thing?

Depends on what pages you're hosting, and how many people are hitting your server with DNS requests. But generally,
no, fairly low-bandwidth EJTP stuff.

## Are there any downsides?

Some specific documents may be bandwidth- or disk-intensive, like the TLD.

## How close is this to completion?

Hard to say, I've only just started it (though I have some very strong design ideas, so it's more a matter of implementing
those and filling in the gaps than figuring it all out as I go). Quite a bit of the work will be handled "invisibly" by
the DEJE library project, and most of the remainder is setting up the DNS server face of it, and the document
structure specifics.

So basically, I have no idea, and refuse to make any sort of promises about deadlines, until I'm quite confident in my
ability to acheive them without running into unexpected complications.

## Is this anything like CJDNS?

No, and the confusion is mostly on the part of CJD for naming his really cool software in a really misleading way. CJDNS
stands for CJD's Networking Suite, and doesn't do DNS at all. DJDNS stands for DEJE DNS, and DNS is all it does.
You can think of it as *CJD NS* vs *DJ DNS*.
