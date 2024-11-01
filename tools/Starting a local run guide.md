# Starting a run on local ML-OPS Platform

## Step 0: Cloning the main repo, setting up Docker and creating a SSH connection to GitHub

Clone the main repository to your local folder:

```
git clone https://github.com/Softala-MLOPS/oss-mlops-platform.git
```
For Windows machines you need a WSL environtment and it's linux commandline.

https://learn.microsoft.com/en-us/windows/wsl/install

You also need Docker working on your machine.

https://www.docker.com/products/docker-desktop/

You need to have SSH key added to GitHub for multiple steps. USE ONE WITHOUT THE PASSPHRASE.

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

## Step 1: Installing local ML-OPS platform

Run the setup script in the main repository's folder:

```
setup.sh
```
For local installation you want the stand alone kfp and kserve and tell the installer no to the docker registry and Ray questions. The installation will take time and some of the pods can get stuck. You can delete them and they are spun up again in a working manner hopefully.

Checking the pods:

```
kubectl get pods --all-namespaces
```

Deleting a pod:
```
kubectl delete pod -n kubeflow <pod_name>
```
Once you get all the pods running they should start up correctly each time you start the cluster again.

The guides for this are scattered in here https://github.com/Softala-MLOPS/oss-mlops-platform/tree/main/tutorials/local_deployment but they predate the installer which is prefered to be used.

## Step 2 Portforwarding the Kubeflow ports

Every time you start up the cluster you have to portforward the ports from inside the containers so they can be accessed from for example your browser.

Forward the ports:
```
kubectl -n mlflow port-forward svc/mlflow 5000:5000
```

```
kubectl port-forward svc/ml-pipeline-ui -n kubeflow 8080:80
```

After this step you should be able to connect to the Kubeflow interface from http://localhost:8080/

The default email address is `user@example.com` and the default password is `12341234`.

## Step 3 Creating the working repositories

Run the CLI tool located in https://github.com/Softala-MLOPS/oss-mlops-platform/tree/main/tools/CLI-tool

```
python setup_cli.py
```
**TODO: Add more in detail steps**

## Step 4 Installing GitHub Actions runner

You also need a local-hosted GitHub Actions runner which is provided by GitHub.

1. Navigate to your working repo's `Settings` in GitHub web page.
2. Open the `Actions` dropdown menu from the left side of the page under Code and automation.
3. Select the `Runners`
4. Click on the green button that says `New self-hosted runner`
5. Select the appropriate runner image 
   - For Windows select Linux x64 and use the WSL Linux command line
6. Copy and run the commands one by one
7. Afterwards you should have a self-hosted GitHub Actions runner waiting for jobs.

You can restart the runner after the next computer restart by navigating to the runner's `actions-runner/` folder and running:

```
./run.sh
```

## Step 5 Starting the run on local ML-OPS platform

If everything is in order then by pushing to your working repository GitHub should order the runner on your computer to start the run on your computer's Kubeflow setup.