# Query Augmentation Using Relevance Data

## Dependencies
*   **Python3**. Should be already part of Ubuntu's VM. To check run

    ```bash
    which python3       
    ```
    On an Ubuntu 14.04 VM, this should return something like
    `/usr/bin/python3`. If not installed, the following will install Python
    3.6:

    ```bash
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    ```
*  **NumPy** and **SciPy** for Python 3.
    Both packages (though NumPy typically comes with Python3) can be installed
    with `pip`. First upgrade `pip3` on the VM:
    
    ```bash
    sudo -H pip3 install --upgrade pip
    ```

    Then to install the packages for the user, run:

    ```bash
    pip3 install --user numpy scipy
    # may need to add /home/<username>/.local/bin to PATH
    ```

    To install on the VM for all users, run

    ```bash
    sudo -H pip3 install numpy scipy
    # may need to add /home/<username>/.local/bin to PATH
    ```

*   **scikit-learn** for Python3. This has the above packages as a
    dependencies. To install, run the following in a terminal window:

    ```bash
    sudo -H pip3 install -U scikit-learn
    ```
*   **Google API Python Client for Python3**
    Same `pip3` commands as above:

    ```bash
    sudo -H pip3 install --upgrade google-api-python-client
    ```

## Implementation

### VM Pointers
I've set up the VM with all the software that is needed, included the SciPy
modules and the Google APIs. If you want to try the code on the VM, here are
some pointers on setting up things from your terminal:

1.  Download and set up Google SDK on your local machine (laptop). You need
    this to use the `gcloud` CLI. Get the tarball from: <https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-173.0.0-linux-x86_64.tar.gz>

2.  Uncompress in your install directory. This will create the package tree
    `google-cloud-sdk` in there.

3.  Before running the install, edit your shell profile file (e.g.,
    ~/.bash_profile) and add the following

    ```bash
    Add ~/opt/google-cloud-sdk/bin to PATH
    Edit ~/.bash_profile to add the following
    ```
4.  Install `gcloud`. From the `google-cloud-sdk` directory

    ```bash
    $ ./install.sh
    ```

5.  When done. Run `gcloud init`. This is useful information from its output.

You should have the `gcloud` tools now. To start/stop the VM from your
terminal, use the following commands (the name of the VM is `gcvm-1`)

```bash
$ gcloud compute instances start gcvm-1     # to start it
$ gcloud compute instances stop gcvm-1      # to stop it
```

After you get a status from the start command, you can login from you terminal

```bash
gcloud compute ssh gcvm-1
```

`gcloud compute ssh` is a wrapper around your system's `ssh` that'll take care
of your key files' setup. It will use your local user name, given by `$USER`,
to create your `home` directory on the VM. If you want to specify a username
(e.g., rb3074), replace `gcvm-1` with `username@gcvm-1` in the above command.

If you want to use your file browser to move files between your local machine
and the VM (much easier than the command line), go to the Compute Engine page
for our VM:
https://console.cloud.google.com/compute/instances?project=cs6111-181600&duration=PT1H,
and get its IP address. Then in your file browser's address space, enter:

`sftp://<ip-addr>/home/<username>`

Finally, to automate things, add these aliases to your shell login file (e.g.,
~/.bash_aliases) and use them.

```bash
# Start/Stop VM
alias gvm-start='gcloud compute instances start gcvm-1'
alias gvm-stop='gcloud compute instances stop gcvm-1'

alias gvm='gcloud compute ssh gcvm-1'
alias gcp='gcloud compute scp'
```
