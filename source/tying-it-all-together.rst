Tying it all together
------------------------


A comparison of trade-offs of various methods
+++++++++++++++++++++++++++++++++++++++++++++++

=======================     ==========   ==================  ====================================
Method                      Isolation    Time to             Django DB
                                         launch new tenants  Compatibility
=======================     ==========   ==================  ====================================
Shared DB and Schema        Low          Low                 High (Supported in all DBs)
Isolated Schema             Medium       Low                 Medium (DB must support schema)
Isolated DB                 High         Medium              High (Supported in all DBs)
Isolated using docker       Complete     Medium              High (Supported in all DBs)
=======================     ==========   ==================  ====================================



What method should I use?
++++++++++++++++++++++++++++++++++++++++++++

