# 📧 A Toy Model of Cryptographic Signatures 📧

Here is a super simple toy model on how the signing of messages can work. It is probably far from being secure, but it gives the right mental model.

### Modular Rules

Before we start, let's remind ourselves of some mathematical rules when it comes to the modulus. 

$$ (a+b) \\% c = (a\\%c+b\\%c)\\%c $$

$$ (a \cdot b) \\% c = 0 $$

With those two equations, we can easily derive a third one that becomes quite important later:

$$
\begin{align*} 
((a\\%c) \cdot b) \\% c 
&= ((a-nc) \cdot b) \\% c =\\
&= (ab - bnc) \\% c =\\
&= ( [(ab)\\%c] + \underbrace{[(bnc) \\% c]}_{=0} ) \\% c =\\
&= ((ab)\\%c)\\%c = (ab)\\%c
\end{align*}
$$

### Definitions

Before we start, we need an operation that maps an arbitrary message to a number we can calculate with, i.e., we need some hash function. In our case, we simply use modulus:

```
def hash(message):
    return sum(bytearray(message, 'utf-8')) % C
```

Now, let's define two operations, one for signing a message and another one for verifying the signature:

Creating a signature is as simple as multiplying the hashed message with the secret key and then projecting it down to a smaller value range by taking its modulus c. Obviously, this hides the secret key.

$$
\text{sig} := (\text{hash}(\text{msg}) \cdot \text{sk} ) \\% c 
$$

Verifying the signature can be done by comparing the hashed message with the product of the public key and the signature projected by the modulus c operation.

$$
(\text{sig} \cdot \text{pk}) \\% c == \text{hash}(\text{msg})
$$

### How to generate public and secret keys

The above schema obviously does not work for any pair of pk and sk; instead, they need to fulfill a certain criterion. Let's derive which criterion. For that, we simply inject the definition of the signature into the second equation. This yields:

$$
\begin{align*} 
\text{hash}(\text{msg}) 
&= [(\text{hash}(\text{msg}) \cdot \text{sk}) \\% c \cdot \text{pk}] \\% c = \\
&= [\text{hash}(\text{msg}) \cdot \text{sk} \cdot \text{pk}] \\% c = \\
&= [\underbrace{(\text{sk} \cdot \text{pk}) \\% c}_{=1} \cdot \text{hash}(\text{msg}) ]\\% c \\
\end{align*}
$$

For the equation above to hold, we need the secret key to be the multiplicative inverse of the public key in the space spanned by the modulus operation.
