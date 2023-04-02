# Broken Guides

Once we or someone else notices that a guide doesn't work anymore, do the following things:

1. Document that the guide is broken.
    - create an issue stating that the guide is broken. If possible, add details on what exactly is broken.
    - @-mention the original author, notifying them of the broken guide
    - add a banner / warning box to the guide, saying that it might be broken. link the issue.
    - we do not provide support for the broken guide after this point
2. if nobody fixes the guide after 2 months
    - delete the guide
    - add the deleting commit to the issue
    - close the issue

```rst
.. error::

  This guide seems to be **broken** for the current versions of XYZ, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/000
```

```md
The guide for XYZ does not work anymore. [explanation of what does not work here]. We added a banner to the guide to signal the broken state.

If you have any insights, please comment on this issue. Pull requests fixing the guide are also highly appreciated. If the guide does not get fixed within two months, we will remove it from the lab, as documented in the [broken guides policy](https://github.com/Uberspace/lab/blob/main/BROKEN_GUIDES.md).

@[original guide author here] FYI.
```
