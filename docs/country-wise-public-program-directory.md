# Country-wise public security program directory

This directory is for **authorized vulnerability reporting only**. It tracks organizations with an official, public security reporting or bug bounty program—not a list of systems to probe.

## Inclusion rules

Add an organization only when you can link to its official security or bounty page. Record the country only when the organization explicitly publishes a relevant headquarters or security-program location; do not infer it from an app's popularity, user base, domain, or language. Country is organizational context, not permission to test.

Before any testing, read the current program policy and verify that the exact asset and test type are in scope. If scope or permission is unclear, do not test; use the published contact channel to ask. Do not test real users, access or retain data, disrupt services, or publish undisclosed vulnerabilities.

## Entry format

Use one row per organization and keep links to official sources. Mark unknown or unpublished country as `Not stated` rather than guessing.

| Country (officially stated) | Organization / app | Official program or disclosure policy | Program type | Last checked (UTC date) |
|---|---|---|---|---|
| Example Country | Example Organization | https://example.com/security | VDP or bounty | YYYY-MM-DD |

The example row is a format illustration only and is not a real program listing.

## Finding official programs

Start from the organization's own security page or a recognized disclosure platform's public program directory. Confirm the program is still active and follow its linked policy; a listing alone does not grant authorization outside that policy.

## Updating this directory

- Verify each URL and policy from an official source before adding an entry.
- Include a `Last checked` date and revisit links periodically.
- Remove or mark entries that become inactive or whose official policy cannot be verified.
- Do not include guessed contacts, private assets, leaked information, or instructions for testing out-of-scope targets.
