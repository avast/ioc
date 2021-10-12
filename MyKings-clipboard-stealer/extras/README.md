# Script for querying information about how muh crypto money wallets received

Data received should be in a json format where wallet addresses are objects containing information
about them. Information must contain "currency" with a correct tag, because script queries only
one API at a time based on that tag. The "currency" is a list in a case when one address may
belong to multiple cryptocurrencies.
<br/>
<br/>
Example input:

```
{
	"wallet_address" :
	{
		"currency": ["Bitcoin"],
		"samples": [sha1, sha2, sha3, sha4],
		"any_other_info" : "useful information"
	},
	"wallet_address2" :
	{
		"currency": ["Ethereum"]
	}
}
```
<br/>
Script can be run from console with following command:

```
> wallet_gain.py -if ./wallets_tagged.json -of ./wallet_gains.json
```
