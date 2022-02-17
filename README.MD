Simple Token Swap
-----------------
Contract is created by:
```
brownie import TokenSwap

swap_contract = TokenSwap.deploy(
        token_A_contract.address, token_B_contract.address, A_ratio, B_ratio, {"from": accounts[0]}
    )
```
Where `A_ratio` and `B_ratio` define the relationship between the two tokens.
Handling of decimals should be done off-chain, not on-chain, and this is done by adjusting the ratios.
For example, suppose we have House token with 2 decimal places, and a Car token with 5 decimal places.
Also assume that the ratio is 3:20 (3 House tokens for every 20 car tokens).

The contracts internal representation needs to be 300000:2000 (3 * 10 ** 5 : 20 * 10 ** 2).
If I wanted to swap 3 House tokens for 20 Car tokens, I would send a transaction that looked like:
```
tx = swap.swapAforB(300, {"from": user})
```
And the Car Token balance of the user will be 2,000,000 (20 with 5 extra 0's for the decimal places)
