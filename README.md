<div align="center">
<h1 align="center">AlumBot - RAG-GPT</h1>
Quickly launch an intelligent customer service system with Flask, LLM, RAG, including frontend, backend, and admin console.
<br/>
<a href="https://langchain-bot.open-sora.ai/" target="_blank"> Live Demo </a>
<br/>
<img style="display: block; margin: auto; width: 70%;" src="./doc/rag_overview.jpg">
</div>


# Contents

- [Features](#features)
- [Online Retrieval Architecture](#online-retrieval-architecture)
- [Deploy the AlumBot Service](#deploy-the-alumbot-service)
  - [Step 1: Download repository code](#step-1-download-repository-code)
  - [Step 2: Configure variables of .env](#step-2-configure-variables-of-env)
    - [Using OpenAI as the LLM base](#using-openai-as-the-llm-base)
    - [Using ZhipuAI as the LLM base](#using-zhipuai-as-the-llm-base)
    - [Using DeepSeek as the LLM base](#using-deepseek-as-the-llm-base)
    - [Using Moonshot as the LLM base](#using-moonshot-as-the-llm-base)
    - [Using local LLMs](#using-local-llms)
  - [Step 3: Deploy AlumBot](#step-3-deploy-alumbot)
    - [Deploy AlumBot using Docker](#deploy-alumbot-using-docker)
    - [Deploy AlumBot from source code](#deploy-alumbot-from-source-code)
      - [Set up the Python running environment](#set-up-the-python-running-environment)
        - [Create and activate a virtual environment](#create-and-activate-a-virtual-environment)
        - [Install dependencies with pip](#install-dependencies-with-pip)
      - [Create SQLite Database](#create-sqlite-database)
      - [Start the service](#start-the-service)
- [Deploy to Azure Cloud](#deploy-to-azure-cloud)
  - [Prerequisites](#prerequisites)
  - [Step 1: Install and Set Up Azure CLI](#step-1-install-and-set-up-azure-cli)
  - [Step 2: Create an Azure Container Registry (ACR)](#step-2-create-an-azure-container-registry-acr)
  - [Step 3: Build and Push Docker Image to ACR](#step-3-build-and-push-docker-image-to-acr)
  - [Step 4: Deploy to Azure Container Instances (ACI)](#step-4-deploy-to-azure-container-instances-aci)
  - [Step 5: Configure Persistent Storage (Optional)](#step-5-configure-persistent-storage-optional)
  - [Step 6: Update Your Application](#step-6-update-your-application)
  - [Updating the Azure Deployment with Clean Database](#updating-the-azure-deployment-with-clean-database)
  - [Troubleshooting Azure Deployment](#troubleshooting-azure-deployment)
- [Configure the admin console](#configure-the-admin-console)
  - [Login to the admin console](#login-to-the-admin-console)
  - [Import your data](#import-your-data)
    - [import websites](#import-websites)
    - [import isolated urls](#import-isolated-urls)
    - [import local files](#import-local-files)
  - [Test the chatbot](#test-the-chatbot)
  - [Embed on your website](#embed-on-your-website)
  - [Dashboard of user's historical request](#dashboard-of-users-historical-request)
- [The frontend of admin console and chatbot](#the-frontend-of-admin-console-and-chatbot)
  - [admin console](#admin-console)
  - [chatbot](#chatbot)
- [Database Maintenance](#database-maintenance)


## Features
- **Built-in LLM Support**: Support cloud-based LLMs and local LLMs.
- **Quick Setup**: Enables deployment of production-level conversational service robots within just five minutes.
- **Diverse Knowledge Base Integration**: Supports multiple types of knowledge bases, including websites, isolated URLs, and local files.
- **Flexible Configuration**: Offers a user-friendly backend equipped with customizable settings for streamlined management.
- **Attractive UI**: Features a customizable and visually appealing user interface.


## Online Retrieval Architecture

<div align="center">
<img style="display: block; margin: auto; width: 100%;" src="./doc/online_retrieve.jpg">
</div>


## Deploy the AlumBot Service

### Step 1: Download repository code

Clone the repository:

```shell
git clone https://github.com/yourusername/AlumBot.git && cd AlumBot
```

### Step 2: Configure variables of .env

Before starting the AlumBot service, you need to modify the related configurations for the program to initialize correctly. 

#### Using OpenAI as the LLM base

```shell
cp env_of_openai .env
```

The variables in .env

```shell
LLM_NAME="OpenAI"
OPENAI_API_KEY="xxxx"
GPT_MODEL_NAME="gpt-4o-mini"
MIN_RELEVANCE_SCORE=0.4
BOT_TOPIC="ALUMBOT"
URL_PREFIX="http://127.0.0.1:7000/"
USE_PREPROCESS_QUERY=1
USE_RERANKING=1
USE_DEBUG=0
USE_LLAMA_PARSE=0
LLAMA_CLOUD_API_KEY="xxxx"
USE_GPT4O=1
```

- Don't modify **`LLM_NAME`**
- Modify the **`OPENAI_API_KEY`** with your own key. Please log in to the [OpenAI website](https://platform.openai.com/api-keys) to view your API Key.
- Update the **`GPT_MODEL_NAME`** setting, replacing `gpt-4o-mini` with `gpt-4-turbo` or `gpt-4o` if you want to use GPT-4.
- Change **`BOT_TOPIC`** to reflect your Bot's name. This is very important, as it will be used in `Prompt Construction`. Please try to use a concise and clear word, such as `OpenIM`, `LangChain`.
- Adjust **`URL_PREFIX`** to match your website's domain. This is mainly for generating accessible URL links for uploaded local files. Such as `http://127.0.0.1:7000/web/download_dir/2024_05_20/d3a01d6a-90cd-4c2a-b926-9cda12466caf/openssl-cookbook.pdf`.
- Set **`USE_LLAMA_PARSE`** to 1 if you want to use `LlamaParse`.
- Modify the **`LLAMA_CLOUD_API_KEY `** with your own key. Please log in to the [LLamaCloud website](https://cloud.llamaindex.ai/api-key) to view your API Key.
- Set **`USE_GPT4O`** to 1 if you want to use `GPT-4o` mode.
- For more information about the meanings and usages of constants, you can check under the `server/constant` directory.

#### Using ZhipuAI as the LLM base

If you cannot use OpenAI's API services, consider using ZhipuAI as an alternative. 


```shell
cp env_of_zhipuai .env
```

The variables in .env

```shell
LLM_NAME="ZhipuAI"
ZHIPUAI_API_KEY="xxxx"
GLM_MODEL_NAME="glm-4-air"
MIN_RELEVANCE_SCORE=0.4
BOT_TOPIC="ALUMBOT"
URL_PREFIX="http://127.0.0.1:7000/"
USE_PREPROCESS_QUERY=1
USE_RERANKING=1
USE_DEBUG=0
USE_LLAMA_PARSE=0
LLAMA_CLOUD_API_KEY="xxxx"
```

- Don't modify **`LLM_NAME`**
- Modify the **`ZHIPUAI_API_KEY`** with your own key. Please log in to the [ZhipuAI website](https://open.bigmodel.cn/usercenter/apikeys) to view your API Key.
- Update the **`GLM_MODEL_NAME`** setting, the model list is `['glm-3-turbo', 'glm-4', 'glm-4-0520', 'glm-4-air', 'glm-4-airx', 'glm-4-flash']`.
- Change **`BOT_TOPIC`** to reflect your Bot's name. This is very important, as it will be used in `Prompt Construction`. Please try to use a concise and clear word, such as `OpenIM`, `LangChain`.
- Adjust **`URL_PREFIX`** to match your website's domain. This is mainly for generating accessible URL links for uploaded local files. Such as `http://127.0.0.1:7000/web/download_dir/2024_05_20/d3a01d6a-90cd-4c2a-b926-9cda12466caf/openssl-cookbook.pdf`.
- Set **`USE_LLAMA_PARSE`** to 1 if you want to use `LlamaParse`.
- Modify the **`LLAMA_CLOUD_API_KEY `** with your own key. Please log in to the [LLamaCloud website](https://cloud.llamaindex.ai/api-key) to view your API Key.
- For more information about the meanings and usages of constants, you can check under the `server/constant` directory.

#### Using DeepSeek as the LLM base

If you cannot use OpenAI's API services, consider using DeepSeek as an alternative.

> [!NOTE]
> DeepSeek does not provide an `Embedding API`, so here we use ZhipuAI's `Embedding API`.


```shell
cp env_of_deepseek .env
```

The variables in .env

```shell
LLM_NAME="DeepSeek"
ZHIPUAI_API_KEY="xxxx"
DEEPSEEK_API_KEY="xxxx"
DEEPSEEK_MODEL_NAME="deepseek-chat"
MIN_RELEVANCE_SCORE=0.4
BOT_TOPIC="ALUMBOT"
URL_PREFIX="http://127.0.0.1:7000/"
USE_PREPROCESS_QUERY=1
USE_RERANKING=1
USE_DEBUG=0
USE_LLAMA_PARSE=0
LLAMA_CLOUD_API_KEY="xxxx"
```

- Don't modify **`LLM_NAME`**
- Modify the **`ZHIPUAI_API_KEY`** with your own key. Please log in to the [ZhipuAI website](https://open.bigmodel.cn/usercenter/apikeys) to view your API Key.
- Modify the **`DEEPKSEEK_API_KEY`** with your own key. Please log in to the [DeepSeek website](https://platform.deepseek.com/api_keys) to view your API Key.
- Update the **`DEEPSEEK_MODEL_NAME `** setting if you want to use other models of DeepSeek.
- Change **`BOT_TOPIC`** to reflect your Bot's name. This is very important, as it will be used in `Prompt Construction`. Please try to use a concise and clear word, such as `OpenIM`, `LangChain`.
- Adjust **`URL_PREFIX`** to match your website's domain. This is mainly for generating accessible URL links for uploaded local files. Such as `http://127.0.0.1:7000/web/download_dir/2024_05_20/d3a01d6a-90cd-4c2a-b926-9cda12466caf/openssl-cookbook.pdf`.
- Set **`USE_LLAMA_PARSE`** to 1 if you want to use `LlamaParse`.
- Modify the **`LLAMA_CLOUD_API_KEY `** with your own key. Please log in to the [LLamaCloud website](https://cloud.llamaindex.ai/api-key) to view your API Key.
- For more information about the meanings and usages of constants, you can check under the `server/constant` directory.


#### Using Moonshot as the LLM base

If you cannot use OpenAI's API services, consider using Moonshot as an alternative.

> [!NOTE]
> Moonshot does not provide an `Embedding API`, so here we use ZhipuAI's `Embedding API`.


```shell
cp env_of_moonshot .env
```

The variables in .env

```shell
LLM_NAME="Moonshot"
ZHIPUAI_API_KEY="xxxx"
MOONSHOT_API_KEY="xxxx"
MOONSHOT_MODEL_NAME="moonshot-v1-8k"
MIN_RELEVANCE_SCORE=0.4
BOT_TOPIC="ALUMBOT"
URL_PREFIX="http://127.0.0.1:7000/"
USE_PREPROCESS_QUERY=1
USE_RERANKING=1
USE_DEBUG=0
USE_LLAMA_PARSE=0
LLAMA_CLOUD_API_KEY="xxxx"
```

- Don't modify **`LLM_NAME`**
- Modify the **`ZHIPUAI_API_KEY`** with your own key. Please log in to the [ZhipuAI website](https://open.bigmodel.cn/usercenter/apikeys) to view your API Key.
- Modify the **`MOONSHOT_API_KEY`** with your own key. Please log in to the [Moonshot website](https://platform.moonshot.cn/console/api-keys) to view your API Key.
- Update the **`MOONSHOT_MODEL_NAME `** setting if you want to use other models of Moonshot.
- Change **`BOT_TOPIC`** to reflect your Bot's name. This is very important, as it will be used in `Prompt Construction`. Please try to use a concise and clear word, such as `OpenIM`, `LangChain`.
- Adjust **`URL_PREFIX`** to match your website's domain. This is mainly for generating accessible URL links for uploaded local files. Such as `http://127.0.0.1:7000/web/download_dir/2024_05_20/d3a01d6a-90cd-4c2a-b926-9cda12466caf/openssl-cookbook.pdf`.
- Set **`USE_LLAMA_PARSE`** to 1 if you want to use `LlamaParse`.
- Modify the **`LLAMA_CLOUD_API_KEY `** with your own key. Please log in to the [LLamaCloud website](https://cloud.llamaindex.ai/api-key) to view your API Key.
- For more information about the meanings and usages of constants, you can check under the `server/constant` directory.


#### Using local LLMs

If your knowledge base involves **sensitive information** and you prefer not to use cloud-based LLMs, consider using `Ollama` to deploy large models locally.


> [!NOTE]
> First, refer to [ollama](https://github.com/ollama/ollama) to **Install Ollama**, and download the embedding model `mxbai-embed-large` and the LLM model such as `llama3`.


```shell
cp env_of_ollama .env
```

The variables in .env

```shell
LLM_NAME="Ollama"
OLLAMA_MODEL_NAME="xxxx"
OLLAMA_BASE_URL="http://127.0.0.1:11434"
MIN_RELEVANCE_SCORE=0.4
BOT_TOPIC="ALUMBOT"
URL_PREFIX="http://127.0.0.1:7000/"
USE_PREPROCESS_QUERY=1
USE_RERANKING=1
USE_DEBUG=0
USE_LLAMA_PARSE=0
LLAMA_CLOUD_API_KEY="xxxx"
```

- Don't modify **`LLM_NAME`**
- Update the **`OLLAMA_MODEL_NAME `** setting, select an appropriate model from [ollama library](https://ollama.com/library).
- If you have changed the default `IP:PORT` when starting `Ollama`, please update **`OLLAMA_BASE_URL`**. Please pay special attention, only enter the IP (domain) and PORT here, without appending a URI.
- Change **`BOT_TOPIC`** to reflect your Bot's name. This is very important, as it will be used in `Prompt Construction`. Please try to use a concise and clear word, such as `OpenIM`, `LangChain`.
- Adjust **`URL_PREFIX`** to match your website's domain. This is mainly for generating accessible URL links for uploaded local files. Such as `http://127.0.0.1:7000/web/download_dir/2024_05_20/d3a01d6a-90cd-4c2a-b926-9cda12466caf/openssl-cookbook.pdf`.
- Set **`USE_LLAMA_PARSE`** to 1 if you want to use `LlamaParse`.
- Modify the **`LLAMA_CLOUD_API_KEY `** with your own key. Please log in to the [LLamaCloud website](https://cloud.llamaindex.ai/api-key) to view your API Key.
- For more information about the meanings and usages of constants, you can check under the `server/constant` directory.


### Step 3: Deploy AlumBot
#### Deploy AlumBot using Docker

> [!NOTE]
> When deploying with Docker, pay special attention to the host of **URL_PREFIX** in the `.env` file. If using `Ollama`, also pay special attention to the host of **OLLAMA_BASE_URL** in the `.env` file. They need to use the actual IP address of the host machine.


```shell
docker-compose up --build
```

#### Deploy AlumBot from source code

> [!NOTE]
> Please use Python version 3.10.x or above.

##### Set up the Python running environment

It is recommended to install Python-related dependencies in a Python virtual environment to avoid affecting dependencies of other projects.

###### Create and activate a virtual environment

If you have not yet created a virtual environment, you can create one with the following command:

```shell
python -m venv myenv
```

After creation, activate the virtual environment:

```shell
source myenv/bin/activate
 .\myenv\Scripts\Activate.ps1
```

###### Install dependencies with pip

Once the virtual environment is activated, you can use `pip` to install the required dependencies. 

```shell
pip install -r requirements.txt
```

##### Create SQLite Database

The AlumBot service uses SQLite as its storage DB. Before starting the AlumBot service, you need to execute the following command to initialize the database and add the default configuration for admin console.

```shell
python create_sqlite_db.py
```

##### Start the service

If you have completed the steps above, you can try to start the AlumBot service by executing the following command.

- **Start single process:**

```shell
python rag_gpt_app.py
```

- **Start multiple processes:**

```shell
sh start.sh
```

> [!NOTE]
> - The service port for AlumBot is **`7000`**. During the first test, please try not to change the port so that you can quickly experience the entire product process.
> - We recommend starting the AlumBot service using **`start.sh`** in multi-process mode for a smoother user experience.



## Deploy to Azure Cloud

This section provides step-by-step instructions for deploying the AlumBot backend Docker image to Azure Cloud using Azure Container Instances (ACI).

### Prerequisites

Before you begin, make sure you have:

- An active Azure subscription
- The AlumBot code repository on your local machine
- Docker installed on your local development machine
- Basic familiarity with command-line tools

### Step 1: Install and Set Up Azure CLI

1. Download and install the Azure CLI from the official Microsoft website:
   [https://aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)

2. After installation, open a new command prompt or PowerShell window and authenticate with your Azure account:

   ```shell
   az login
   ```

   This will open a browser window where you should sign in with your Azure account credentials.

3. Verify the installation by checking the version:

   ```shell
   az --version
   ```

### Step 2: Create an Azure Container Registry (ACR)

1. Create a resource group to organize all resources for AlumBot:

   ```shell
   az group create --name AlumBotResourceGroup --location eastus
   ```

2. Create an Azure Container Registry to store your Docker images:

   ```shell
   az acr create --resource-group AlumBotResourceGroup --name alumbotreg --sku Basic
   ```

   > Note: Registry names must be unique across Azure. If 'alumbotreg' is already taken, choose a different name.

3. Enable admin access to your registry (needed for ACI to pull images):

   ```shell
   az acr update --name alumbotreg --admin-enabled true
   ```

4. Get the registry credentials for later use:

   ```shell
   az acr credential show --name alumbotreg
   ```

   Save the username and password values for the next steps.

### Step 3: Build and Push Docker Image to ACR

1. Navigate to your AlumBot directory:

   ```shell
   cd path/to/AlumBot
   ```

2. Before building the image, ensure you've updated the `.env` file with the correct configuration for production. In particular, update the `URL_PREFIX` to match your Azure deployment URL:

   ```
   URL_PREFIX="http://your-dns-name-label.region.azurecontainer.io:7000/"
   ```

   For example: `URL_PREFIX="http://alumbot.eastus.azurecontainer.io:7000/"`

3. Log in to your Azure Container Registry:

   ```shell
   az acr login --name alumbotreg
   ```

4. Build and tag your Docker image:

   ```shell
   docker build -t alumbotreg.azurecr.io/alumbot:latest .
   ```

5. Push the image to ACR:

   ```shell
   docker push alumbotreg.azurecr.io/alumbot:latest
   ```

### Step 4: Deploy to Azure Container Instances (ACI)

1. Deploy your AlumBot container to Azure Container Instances:

   ```shell
   az container create \
     --resource-group AlumBotResourceGroup \
     --name alumbot-container \
     --image alumbotreg.azurecr.io/alumbot:latest \
     --dns-name-label alumbot \
     --ports 7000 \
     --registry-username alumbotreg \
     --registry-password <password-from-acr-credentials> \
     --os-type Linux \
     --cpu 1 \
     --memory 1.5
   ```

   > Note: Replace `<password-from-acr-credentials>` with the password you obtained in Step 2.4.
   > 
   > If the `dns-name-label` 'alumbot' is already in use in your region, choose a different name.

2. Check the deployment status:

   ```shell
   az container show \
     --resource-group AlumBotResourceGroup \
     --name alumbot-container \
     --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState,State:instanceView.state}" \
     --out table
   ```

3. Once deployed, your AlumBot will be accessible at:

   ```
   http://alumbot.eastus.azurecontainer.io:7000
   ```

   > Note: Replace 'alumbot' with your actual DNS name label and 'eastus' with your deployment region if different.

### Step 5: Configure Persistent Storage (Optional)

For production deployments, you'll want to set up persistent storage for your databases:

1. Create a storage account:

   ```shell
   az storage account create \
     --resource-group AlumBotResourceGroup \
     --name alumbotstore \
     --location eastus \
     --sku Standard_LRS
   ```

2. Get the storage account key:

   ```shell
   az storage account keys list \
     --resource-group AlumBotResourceGroup \
     --account-name alumbotstore \
     --query "[0].value" \
     --output tsv
   ```

3. Create a file share:

   ```shell
   az storage share create \
     --name alumbot-data \
     --account-name alumbotstore \
     --account-key <storage-key>
   ```

4. Recreate your container with persistent storage:

   ```shell
   az container create \
     --resource-group AlumBotResourceGroup \
     --name alumbot-container \
     --image alumbotreg.azurecr.io/alumbot:latest \
     --dns-name-label alumbot \
     --ports 7000 \
     --registry-username alumbotreg \
     --registry-password <password> \
     --os-type Linux \
     --cpu 1 \
     --memory 1.5 \
     --azure-file-volume-account-name alumbotstore \
     --azure-file-volume-account-key <storage-key> \
     --azure-file-volume-share-name alumbot-data \
     --azure-file-volume-mount-path /app/data
   ```

   You may need to modify your application to use the `/app/data` directory for storing SQLite databases and other persistent data.

### Step 6: Update Your Application

When you need to deploy updates to your AlumBot application:

1. Make your code changes locally

2. For the AlumBot-Client, create a `.env.production` file with the appropriate settings:

   ```
   # Production environment
   VITE_BASE_URL=http://alumbot.eastus.azurecontainer.io:7000/
   ```

3. Build and push the updated Docker image:

   ```shell
   docker build -t alumbotreg.azurecr.io/alumbot:latest .
   az acr login --name alumbotreg
   docker push alumbotreg.azurecr.io/alumbot:latest
   ```

4. Restart or recreate your container to apply the changes:

   ```shell
   # Option 1: Restart the container (if the image tag hasn't changed)

   az container restart --resource-group AlumBotResourceGroup --name alumbot-container
   
   # Option 2: Recreate the container (to force pulling the new image)
   az container delete --resource-group AlumBotResourceGroup --name alumbot-container --yes
   az container create --resource-group AlumBotResourceGroup --name alumbot-container --image alumbotreg.azurecr.io/alumbot:latest --dns-name-label alumbot --ports 7000 --registry-username alumbotreg --registry-password <password> --os-type Linux --cpu 1 --memory 1.5
   ```

### Troubleshooting Azure Deployment

Here are solutions to common issues you might encounter during deployment:

1. **Resource Provider Not Registered**

   If you receive an error about "MissingSubscriptionRegistration" for Microsoft.ContainerInstance:

   ```shell
   az provider register --namespace Microsoft.ContainerInstance
   ```

   Wait a few minutes for the registration to complete before trying again.

2. **Container OS Type Error**

   If you see an error about invalid OS type:

   ```
   (InvalidOsType) The 'osType' for container group is invalid
   ```

   Make sure to include the `--os-type Linux` parameter in your `az container create` command.

3. **Resource Requests Not Specified**

   If you receive an error about resource requests not being specified:

   ```
   (ResourceRequestsNotSpecified) The resource requests are not specified
   ```

   Include the `--cpu` and `--memory` parameters in your `az container create` command.

4. **Unable to Connect to Your Container**

   If you can't connect to your deployed container, check:
   
   - Verify the container is running: `az container show --resource-group AlumBotResourceGroup --name alumbot-container --query "instanceView.state"`
   - Check container logs: `az container logs --resource-group AlumBotResourceGroup --name alumbot-container`
   - Confirm port 7000 is exposed and accessible

5. **Case-Sensitivity URL Issues**

   If you encounter issues with URLs being case-sensitive (e.g., `/alumBot` vs `/alumbot`), update your routes in `rag_gpt_app.py` to handle both cases as shown below:

   ```python
   # Add lowercase route handlers alongside the original case-sensitive routes
   @app.route('/alumbot', strict_slashes=False)
   def index_chatbot_lowercase():
       return send_from_directory(f'{app.static_folder}/alumBot', 'index.html')

   @app.route('/alumbot/<path:path>')
   def serve_static_chatbot_lowercase(path):
       return send_from_directory(f'{app.static_folder}/alumBot', path)
   ```


## Configure the admin console

### Login to the admin console

Access the admin console through the link **`http://your-server-ip:7000/alumbot-admin/`** to reach the login page. The default username and password are **`admin`** and **`alumBot_AIGC@2024`** (can be checked in `create_sqlite_db.py`).

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-2.jpg">
</div>

After logging in successfully, you will be able to see the configuration page of the admin console.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-3.jpg">
</div>

On the page **`http://your-server-ip:7000/alumbot-admin/#/`**, you can set the following configurations:
- Choose the LLM base, currently only the `gpt-3.5-turbo` option is available, which will be gradually expanded.
- Initial Messages
- Suggested Messages
- Message Placeholder
- Profile Picture (upload a picture)
- Display name
- Chat icon (upload a picture)

### Import your data

#### Import websites

After submitting the website URL, once the server retrieves the list of all web page URLs via crawling, you can select the web page URLs you need as the knowledge base (all selected by default). The initial `Status` is **`Recorded`**.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-12.jpg">
</div>

You can actively refresh the page **`http://your-server-ip:7000/alumbot-admin/#/source`** in your browser to get the progress of web page URL processing. After the content of the web page URL has been crawled, and the Embedding calculation and storage are completed, you can see the corresponding `Size` in the admin console, and the `Status` will also be updated to **`Trained`**.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-13.jpg">
</div>

Clicking on a webpage's URL reveals how many sub-pages the webpage is divided into, and the text size of each sub-page.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-10.jpg">
</div>

Clicking on a sub-page allows you to view its full text content. This will be very helpful for verifying the effects during the experience testing process.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-11.jpg">
</div>

#### Import isolated urls

Collect the URLs of the required web pages. You can submit up to `10` web page URLs at a time, and these pages can be from different domains.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-14.jpg">
</div>

#### Import local files

Upload the required local files. You can upload up to `10` files at a time, and each file cannot exceed `30MB`. The following file types are currently supported: `[".txt", ".md", ".pdf", ".epub", ".mobi", ".html", ".docx", ".pptx", ".xlsx", ".csv"]`.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-15.jpg">
</div>


### Test the chatbot

After importing website data in the admin console, you can experience the chatbot service through the link **`http://your-server-ip:7000/alumBot/`**.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-6.jpg">
</div>

### Embed on your website

Through the admin console link **`http://your-server-ip:7000/alumbot-admin/#/embed`**, you can see the detailed tutorial for configuring the iframe in your website.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-7.jpg">
</div>

<div align="center">
<br/>
<a href="https://docs.openim.io/" target="_blank"> OpenIM chatbot </a>
<br/>
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-8.jpg">
</div>

### Dashboard of user's historical request

Through the admin console link **`http://your-server-ip:7000/alumbot-admin/#/dashboard`**, you can view the historical request records of all users within a specified time range.

<div align="center">
<img style="display: block; margin: auto; width: 70%;" src="./doc/screenshot-9.jpg">
</div>


## The frontend of admin console and chatbot
The AlumBot service integrates 2 frontend modules:

### admin console> [Code Repository](https://github.com/open-kf/smart-qa-admin)

An intuitive web-based admin interface for Smart QA Service, offering comprehensive control over content, configuration, and user interactions. Enables effortless management of the knowledge base, real-time monitoring of queries and feedback, and continuous improvement based on user insights.

### chatbot
> [Code Repository](https://github.com/open-kf/smart-qa-h5)

An HTML5 interface for Smart QA Service designed for easy integration into websites via iframe, providing users direct access to a tailored knowledge base without leaving the site, enhancing functionality and immediate query resolution.

## Database Maintenance

AlumBot includes utility scripts to help you manage and clean the databases when needed. These scripts provide a safe way to reset your system while preserving essential settings.

### Cleaning the Database

If you need to clean your database (for example, when refreshing your knowledge base or resolving issues), you can use the included cleaning scripts:

```shell
python clean_all_databases.py
```

This comprehensive cleaning tool will:

1. **Back up your current database** before making any changes
2. **Clean the SQLite database** - removes content data while preserving user accounts and settings
3. **Clean the Chroma vector database** - removes document embeddings
4. **Clean downloaded files** - removes all files from the `web/download_dir` folder

> [!IMPORTANT]
> Always make sure AlumBot is not running when performing database maintenance operations.

After cleaning, you'll need to repopulate your knowledge base using the admin interface. Your user accounts, bot configuration, and manual interventions will remain intact.

### Individual Cleaning Scripts

You can also use the individual scripts for more targeted cleaning:

- **`clean_database.py`** - Clean only the SQLite database
- **`clean_chroma_db.py`** - Clean only the Chroma vector database

Each script will create a backup before making changes, ensuring you can restore your data if needed.
