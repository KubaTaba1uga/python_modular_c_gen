# What is project about?

1. How test static functions without including c files?
2. How mock any function without stubs?

Idea is that any file has to contain private ops. These ops are available publicly only for tests.

About not static functions (aka public ops) there are two ways to go, one can modularize them as well
  or leave them not modularized. Myself prefer first one.
