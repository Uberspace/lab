.. code-block:: console

 [isabell@stardust ~]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9000
 [isabell@stardust ~]$

Write the port down. In our example it is 9000. In reality you'll get a free port between 61000 and 65535.
