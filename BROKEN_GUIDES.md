# Broken Guides

Once we or someone else notices that a guide doesn't work anymore, do the following things:

1. Document that the guide is broken.
    * create an issue stating that the guide is broken. If possible, add details on what exactly is broken.
    * @-mention the original author, notifying them of the broken guide
    * add a banner / warning box to the guide, saying that it might be broken. link the issue.
2. if nobody fixes the guide after 2 months
    * delete the guide
    * add the deleting commit to the issue
    * close the issue

```rst
.. error::

  This guide seems to be **broken** for the current versions of XYZ, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/000
```
