---


---

<h2 id="ofbuscated-hackivitycon-ctf-2020">OFBuscated HackivityCon CTF 2020</h2>
<p>I just learned some lesser used AES versions and decided to make my own!<br>
<code>nc jh2i.com 50028</code><br>
<a href="https://github.com/AlekhAvinash/Crypto-Solutions/blob/master/ofbuscated.py">ofbuscated.py</a></p>
<hr>
<p><strong>Encryption Method</strong></p>
<ol>
<li>The handle function seems to assert length of flag as:<br>
<code>assert len(flag) % 16 == 1</code></li>
<li>Next the shuffle function pads the string as 16 byte blocks and<br>
shuffles the blocks in random order.</li>
<li>Lastly the string is encrypted using AES OFB method using the same key and IV every time.<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/OFB_encryption.svg/1920px-OFB_encryption.svg.png" alt="enter image description here"></li>
</ol>
<hr>
<p><strong>Exploit</strong></p>
<ol>
<li>From the first step of the encryption process, we learn that the string is of the size <code>16*k + 1</code> since the padding is done by standard method we know the last block as <code>last_block = } + len(string)*15</code></li>
<li>From the length of the output string the we can correctly determine k as 2. This implies that there are 3 blocks one of which is known to us. Since the same key and IV is used we can use the oracle to generate all 3 possible variations.
<ol>
<li><code>m(t)+1st block</code></li>
<li><code>m(t)+2nd block</code></li>
<li><code>m(t)+3rd block</code></li>
</ol>
</li>
<li>Now if we xor every 2 elements and then xor the known 3rd element with 3 output blocks we can decrypt the full flag!!<br>
<a href="https://github.com/AlekhAvinash/Crypto-Solutions/blob/master/exploit.py">exploit.py</a></li>
</ol>

