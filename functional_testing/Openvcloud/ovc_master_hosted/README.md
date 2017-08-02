## OpenvCloud Functional Tests Hosted on ovc_master

All OpenvCloud functional tests designed to run on ovc_master are documented [here](/docs/functional/openvcloud/ovc_master_hosted/ovc_master_hosted.md).

Below only **internal** documentation please.

## Continues Integration

OpenvCloud Testsuite runs continuously on [Jenkins CI](http://ci.codescalers.com/view/Integration%20Testing/)

## Instructions on how to update the coverage documentation

#### Prerequisites

* This instruction works for UNIX-Like operating systems
* Make sure that *pip* and *virtualenv* are installed to your system

    ```shell
    $ sudo apt-get install python-pip
    $ sudo pip install virtualenv
    ```


#### Steps to update

1. Pull the testsuite repository:

  ```
  git clone git@github.com:0-complexity/G8_testing.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/
  ```

3. Run the build script to generate the documentation locally:

  ```
  $ bash functional_testing/Openvcloud/tools/build_docs.sh
  ```

4. Open the documentation using any browser

  ```
  $ firefox auto_generated_docs/_build/html/index.html
  ```
