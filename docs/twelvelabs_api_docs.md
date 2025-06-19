# Twelve Labs API Documentation

*Generated on 2025-06-18 09:33:41*

## Table of Contents

- [Guides](#guides)
  - [Search](#search)
  - [Search](#search)
  - [Analyze videos](#analyze-videos)
  - [Create embeddings](#create-embeddings)
  - [Search](#search)
  - [Analyze videos](#analyze-videos)
  - [Create embeddings](#create-embeddings)
  - [Search with text and image queries](#search-with-text-and-image-queries)
  - [Image embeddings](#image-embeddings)
  - [Open-ended analysis](#open-ended-analysis)
- [Concepts](#concepts)
  - [Models](#models)
  - [Models](#models)
  - [Indexes](#indexes)
  - [Tasks](#tasks)
  - [Modalities](#modalities)
  - [Multimodal large language models](#multimodal-large-language-models)
  - [Marengo](#marengo)
  - [Pegasus](#pegasus)
  - [Indexes](#indexes)
  - [Marengo](#marengo)
  - [Models](#models)
  - [Modalities](#modalities)
- [API Reference](#api-reference)
  - [Introduction](#introduction)
  - [Introduction](#introduction)
  - [Introduction](#introduction)
  - [Make any-to-video search requests](#make-any-to-video-search-requests)
  - [Authentication](#authentication)
  - [Typical workflows](#typical-workflows)
  - [Manage indexes](#manage-indexes)
  - [Upload videos](#upload-videos)
  - [Manage videos](#manage-videos)
  - [Any-to-video search](#any-to-video-search)
  - [Create video embeddings](#create-video-embeddings)
  - [Create text, image, and audio embeddings](#create-text-image-and-audio-embeddings)
  - [Analyze videos](#analyze-videos)
  - [Error codes](#error-codes)
  - [Error codes](#error-codes)
  - [Create embeddings for text, image, and audio](#create-embeddings-for-text-image-and-audio)
  - [Create a video embedding task](#create-a-video-embedding-task)
  - [Create a video indexing task](#create-a-video-indexing-task)
  - [Open-ended analysis](#open-ended-analysis)
  - [Summaries, chapters, or highlights](#summaries-chapters-or-highlights)
  - [Retrieve video information](#retrieve-video-information)
- [Resources](#resources)
  - [Platform overview](#platform-overview)
  - [Sample applications](#sample-applications)
  - [Partner integrations](#partner-integrations)
  - [Platform overview](#platform-overview)
  - [Playground](#playground)
  - [TwelveLabs SDKs](#twelvelabs-sdks)
  - [Frequently asked questions](#frequently-asked-questions)
  - [From the community](#from-the-community)
  - [Migration guide](#migration-guide)
  - [TwelveLabs SDKs](#twelvelabs-sdks)
  - [Adobe Premiere Pro Plugin](#adobe-premiere-pro-plugin)
  - [ApertureDB - Semantic video search engine](#aperturedb---semantic-video-search-engine)
  - [Chroma - Multimodal RAG: Chat with Videos](#chroma---multimodal-rag-chat-with-videos)
  - [Databricks - Advanced video understanding](#databricks---advanced-video-understanding)
  - [Milvus - Advanced video search](#milvus---advanced-video-search)
  - [MindsDB - The TwelveLabs handler](#mindsdb---the-twelvelabs-handler)
  - [MongoDB - Semantic video search](#mongodb---semantic-video-search)
  - [Oracle - Unleashing Video Intelligence](#oracle---unleashing-video-intelligence)
  - [Pinecone - Multimodal RAG](#pinecone---multimodal-rag)
  - [Qdrant - Building a semantic video search workflow](#qdrant---building-a-semantic-video-search-workflow)
  - [Snowflake - Multimodal Video Understanding](#snowflake---multimodal-video-understanding)
  - [Vespa - Multivector video retrieval](#vespa---multivector-video-retrieval)
  - [Voxel51 - Semantic video search plugin](#voxel51---semantic-video-search-plugin)
  - [Weaviate - Leveraging RAG for Improved Video Processing Times](#weaviate---leveraging-rag-for-improved-video-processing-times)
  - [Migration guide](#migration-guide)

---

## Guides {#guides}

### Search {#search}

*Source: https://docs.twelvelabs.io/docs/guides*

#### Import the SDK and initialize the client

Create a client instance to interact with the TwelveLabs Video Understanding platform. Function call: You call the constructor of the TwelveLabs class. Parameters:

- api_key: The API key to authenticate your requests to the platform.

Return value: An object of type TwelveLabs configured for making API calls.

#### Specify the index containing your videos

Indexes help you organize and search through related videos efficiently. This example creates a new index, but you can also use an existing index by specifying its unique identifier. See the Indexes page for more details on creating an index. Function call: You call the index.create function. Parameters:

- name: The name of the index.
- models: An object specifying your model configuration. This example enables the Marengo video understanding model and the visual and audio model options.

Return value: An object containing, among other information, a field named id representing the unique identifier of the newly created index.

#### Upload videos

To perform any downstream tasks, you must first upload your videos, and the platform must finish processing them. Function call: You call the task.create function. This starts a video indexing task, which is an object of type Task that tracks the status of your video upload and indexing process. Parameters:

- index_id: The unique identifier of your index.
- file or url: The path or the publicly accessible URL of your video file.

Return value: An object of type Task containing, among other information, the following fields:

- video_id: The unique identifier of your video
- status: The status of your video indexing task.

#### Monitor the indexing process

The platform requires some time to index videos. Check the status of the video indexing task until it’s completed. Function call: You call the task.wait_for_done function. Parameters:

- sleep_interval: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
- callback: A callback function that the SDK executes each time it checks the status. Note that the callback function takes a parameter of type Task representig the video indexing task you’ve created in the previous step. Use it to display the status of your video indexing task.

Return value: An object containing, among other information, a field named status representing the status of your task. Wait until the value of this field is ready.

#### Perform a search request

Perform a search within your index using a text or image query.

#### Process the search results

Display the search results, including handling pagination to retrieve all pages. Function call: Iterate over the results by calling the next function. Parameters: The search results retrieved in the previous step.

Return value: The next page or raises a StopIteration exception if the iterator has reached the last page.

##### Search with text and image queries

#### Code Examples

```plaintext
$pip install twelvelabs
```

```plaintext
$pip install twelvelabs
```

```plaintext
<>
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
TwelveLabs
```

```plaintext
api_key
```

```plaintext
TwelveLabs
```

```plaintext
index.create
```

```plaintext
name
```

```plaintext
models
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
id
```

```plaintext
task.create
```

```plaintext
Task
```

```plaintext
index_id
```

```plaintext
file
```

```plaintext
url
```

```plaintext
Task
```

```plaintext
video_id
```

```plaintext
status
```

```plaintext
task.wait_for_done
```

```plaintext
sleep_interval
```

```plaintext
callback
```

```plaintext
Task
```

```plaintext
status
```

```plaintext
ready
```

```plaintext
search.query
```

```plaintext
index_id
```

```plaintext
query_text
```

```plaintext
options
```

```plaintext
operator
```

```plaintext
data
```

```plaintext
video_id
```

```plaintext
start
```

```plaintext
end
```

```plaintext
score
```

```plaintext
page_info
```

```plaintext
pool
```

```plaintext
next
```

```plaintext
StopIteration
```


---

### Analyze videos {#analyze-videos}

*Source: https://docs.twelvelabs.io/docs/guides/analyze-videos*

##### Titles, topics, and hashtags

#### Code Examples

```plaintext
/generate
```

```plaintext
/analyze
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
visual
```


---

### Create embeddings {#create-embeddings}

*Source: https://docs.twelvelabs.io/docs/guides/create-embeddings*

##### Video embeddings


---

### Image embeddings {#image-embeddings}

*Source: https://docs.twelvelabs.io/docs/guides/create-embeddings/image*

#### Import the SDK and initialize the client

Create a client instance to interact with the TwelveLabs Video Understanding platform. Function call: You call the constructor of the TwelveLabs class. Parameters:

- api_key: The API key to authenticate your requests to the platform.

Return value: An object of type TwelveLabs configured for making API calls.

#### Create image embeddings

Function call: You call the embed.create function. Parameters:

- model_name: The name of the model you want to use (“Marengo-retrieval-2.7”).
- image_file or image_url: The path or the publicly accessible URL of your image file.

Return value: The response contains the following fields:

- image_embedding: An object that contains the embedding data for your image file. It includes the following fields: segments: An object that contains the following: float: An array of floats representing the embedding metadata: An object that contains metadata about the embedding.
- segments: An object that contains the following: float: An array of floats representing the embedding
- float: An array of floats representing the embedding
- metadata: An object that contains metadata about the embedding.
- model_name: The name ofhe video understanding model the platform has used to create this embedding.

#### Process the results

This example prints the results to the standard output.

##### Models

#### Code Examples

```plaintext
$pip install twelvelabs
```

```plaintext
$pip install twelvelabs
```

```plaintext
<>
```

```plaintext
1from twelvelabs import TwelveLabs2from typing import List3from twelvelabs.models.embed import SegmentEmbedding45# 1. Initialize the client6client = TwelveLabs(api_key="<YOUR_API_KEY>")78# 2. Create image embeddings9res = client.embed.create(10model_name="Marengo-retrieval-2.7", image_url="<YOUR_IMAGE_URL>")1112# 3. Process the results13print(f"Created image embedding: model_name={res.model_name}")14def print_segments(segments: List[SegmentEmbedding], max_elements: int = 5):15for segment in segments:16print(f"  embeddings: {segment.embeddings_float[:max_elements]}")1718if res.image_embedding is not None and res.image_embedding.segments is not None:19print_segments(res.image_embedding.segments)
```

```plaintext
1from twelvelabs import TwelveLabs2from typing import List3from twelvelabs.models.embed import SegmentEmbedding45# 1. Initialize the client6client = TwelveLabs(api_key="<YOUR_API_KEY>")78# 2. Create image embeddings9res = client.embed.create(10model_name="Marengo-retrieval-2.7", image_url="<YOUR_IMAGE_URL>")1112# 3. Process the results13print(f"Created image embedding: model_name={res.model_name}")14def print_segments(segments: List[SegmentEmbedding], max_elements: int = 5):15for segment in segments:16print(f"  embeddings: {segment.embeddings_float[:max_elements]}")1718if res.image_embedding is not None and res.image_embedding.segments is not None:19print_segments(res.image_embedding.segments)
```

```plaintext
TwelveLabs
```

```plaintext
api_key
```

```plaintext
TwelveLabs
```

```plaintext
embed.create
```

```plaintext
model_name
```

```plaintext
image_file
```

```plaintext
image_url
```

```plaintext
image_embedding
```

```plaintext
segments
```

```plaintext
float
```

```plaintext
metadata
```

```plaintext
model_name
```


---

### Search {#search}

*Source: https://docs.twelvelabs.io/docs/guides/search#process-the-search-results*

#### Import the SDK and initialize the client

Create a client instance to interact with the TwelveLabs Video Understanding platform. Function call: You call the constructor of the TwelveLabs class. Parameters:

- api_key: The API key to authenticate your requests to the platform.

Return value: An object of type TwelveLabs configured for making API calls.

#### Specify the index containing your videos

Indexes help you organize and search through related videos efficiently. This example creates a new index, but you can also use an existing index by specifying its unique identifier. See the Indexes page for more details on creating an index. Function call: You call the index.create function. Parameters:

- name: The name of the index.
- models: An object specifying your model configuration. This example enables the Marengo video understanding model and the visual and audio model options.

Return value: An object containing, among other information, a field named id representing the unique identifier of the newly created index.

#### Upload videos

To perform any downstream tasks, you must first upload your videos, and the platform must finish processing them. Function call: You call the task.create function. This starts a video indexing task, which is an object of type Task that tracks the status of your video upload and indexing process. Parameters:

- index_id: The unique identifier of your index.
- file or url: The path or the publicly accessible URL of your video file.

Return value: An object of type Task containing, among other information, the following fields:

- video_id: The unique identifier of your video
- status: The status of your video indexing task.

#### Monitor the indexing process

The platform requires some time to index videos. Check the status of the video indexing task until it’s completed. Function call: You call the task.wait_for_done function. Parameters:

- sleep_interval: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
- callback: A callback function that the SDK executes each time it checks the status. Note that the callback function takes a parameter of type Task representig the video indexing task you’ve created in the previous step. Use it to display the status of your video indexing task.

Return value: An object containing, among other information, a field named status representing the status of your task. Wait until the value of this field is ready.

#### Perform a search request

Perform a search within your index using a text or image query.

#### Process the search results

Display the search results, including handling pagination to retrieve all pages. Function call: Iterate over the results by calling the next function. Parameters: The search results retrieved in the previous step.

Return value: The next page or raises a StopIteration exception if the iterator has reached the last page.

##### Search with text and image queries

#### Code Examples

```plaintext
$pip install twelvelabs
```

```plaintext
$pip install twelvelabs
```

```plaintext
<>
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
TwelveLabs
```

```plaintext
api_key
```

```plaintext
TwelveLabs
```

```plaintext
index.create
```

```plaintext
name
```

```plaintext
models
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
id
```

```plaintext
task.create
```

```plaintext
Task
```

```plaintext
index_id
```

```plaintext
file
```

```plaintext
url
```

```plaintext
Task
```

```plaintext
video_id
```

```plaintext
status
```

```plaintext
task.wait_for_done
```

```plaintext
sleep_interval
```

```plaintext
callback
```

```plaintext
Task
```

```plaintext
status
```

```plaintext
ready
```

```plaintext
search.query
```

```plaintext
index_id
```

```plaintext
query_text
```

```plaintext
options
```

```plaintext
operator
```

```plaintext
data
```

```plaintext
video_id
```

```plaintext
start
```

```plaintext
end
```

```plaintext
score
```

```plaintext
page_info
```

```plaintext
pool
```

```plaintext
next
```

```plaintext
StopIteration
```


---

### Search with text and image queries {#search-with-text-and-image-queries}

*Source: https://docs.twelvelabs.io/docs/guides/search/search-with-text-and-image-queries*

##### Query engineering


---

### Analyze videos {#analyze-videos}

*Source: https://docs.twelvelabs.io/v1.3/docs/guides/analyze-videos*

##### Titles, topics, and hashtags

#### Code Examples

```plaintext
/generate
```

```plaintext
/analyze
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
visual
```


---

### Open-ended analysis {#open-ended-analysis}

*Source: https://docs.twelvelabs.io/v1.3/docs/guides/analyze-videos/open-ended-analysis*

#### Import the SDK and initialize the client

Create a client instance to interact with the TwelveLabs Video Understanding platform. Function call: You call the constructor of the TwelveLabs class. Parameters:

- api_key: The API key to authenticate your requests to the platform.

Return value: An object of type TwelveLabs configured for making API calls.

#### Specify the index containing your videos

Indexes help you organize and search through related videos efficiently. This example creates a new index, but you can also use an existing index by specifying its unique identifier. See the Indexes page for more details on creating an index. Function call: You call the index.create function. Parameters:

- name: The name of the index.
- models: An object specifying your model configuration. This example enables the Pegasus video understanding model and the visual and audio model options.

Return value: An object containing, among other information, a field named id representing the unique identifier of the newly created index.

#### Upload videos

To perform any downstream tasks, you must first upload your videos, and the platform must finish processing them. Function call: You call the task.create function. This starts a video indexing task, which is an object of type Task that tracks the status of your video upload and indexing process. Parameters:

- index_id: The unique identifier of your index.
- file or url: The path or the publicly accessible URL of your video file.

Return value: An object of type Task containing, among other information, the following fields:

- video_id: The unique identifier of your video
- status: The status of your video indexing task.

#### Monitor the indexing process

The platform requires some time to index videos. Check the status of the video indexing task until it’s completed. Function call: You call the task.wait_for_done function. Parameters:

- sleep_interval: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
- callback: A callback function that the SDK executes each time it checks the status. Note that the callback function takes a parameter of type Task representig the video indexing task you’ve created in the previous step. Use it to display the status of your video indexing task.

Return value: An object containing, among other information, a field named status representing the status of your task. Wait until the value of this field is ready.

#### Perform open-ended analysis

#### Process the results

##### Prompt examples

#### Code Examples

```plaintext
stream_start
```

```plaintext
text_generation
```

```plaintext
stream_end
```

```plaintext
text_stream.aggregated_text
```

```plaintext
$pip install twelvelabs
```

```plaintext
$pip install twelvelabs
```

```plaintext
<>
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [9{10"name": "pegasus1.2",11"options": ["visual", "audio"]12}13]14index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)15print(f"Index created: id={index.id}, name={index.name}")1617# 3. Upload a video18task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")19print(f"Task id={task.id}, Video id={task.video_id}")2021# 4. Monitor the indexing process22def on_task_update(task: Task):23print(f"  Status={task.status}")24task.wait_for_done(sleep_interval=5, callback=on_task_update)2526if task.status != "ready":27raise RuntimeError(f"Indexing failed with status {task.status}")28print(f"The unique identifier of your video is {task.video_id}.")2930# 5. Generate open-ended text31text_stream = client.analyze_stream(32video_id=task.video_id, prompt="<YOUR_PROMPT>", temperature=0.2)3334# 6. Process the results35for text in text_stream:36print(text)37print(f"Aggregated text: {text_stream.aggregated_text}")
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [9{10"name": "pegasus1.2",11"options": ["visual", "audio"]12}13]14index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)15print(f"Index created: id={index.id}, name={index.name}")1617# 3. Upload a video18task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")19print(f"Task id={task.id}, Video id={task.video_id}")2021# 4. Monitor the indexing process22def on_task_update(task: Task):23print(f"  Status={task.status}")24task.wait_for_done(sleep_interval=5, callback=on_task_update)2526if task.status != "ready":27raise RuntimeError(f"Indexing failed with status {task.status}")28print(f"The unique identifier of your video is {task.video_id}.")2930# 5. Generate open-ended text31text_stream = client.analyze_stream(32video_id=task.video_id, prompt="<YOUR_PROMPT>", temperature=0.2)3334# 6. Process the results35for text in text_stream:36print(text)37print(f"Aggregated text: {text_stream.aggregated_text}")
```

```plaintext
TwelveLabs
```

```plaintext
api_key
```

```plaintext
TwelveLabs
```

```plaintext
index.create
```

```plaintext
name
```

```plaintext
models
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
id
```

```plaintext
task.create
```

```plaintext
Task
```

```plaintext
index_id
```

```plaintext
file
```

```plaintext
url
```

```plaintext
Task
```

```plaintext
video_id
```

```plaintext
status
```

```plaintext
task.wait_for_done
```

```plaintext
sleep_interval
```

```plaintext
callback
```

```plaintext
Task
```

```plaintext
status
```

```plaintext
ready
```

```plaintext
analyze_stream
```

```plaintext
video_id
```

```plaintext
prompt
```

```plaintext
temperature
```

```plaintext
texts
```

```plaintext
aggregated_text
```

```plaintext
aggregated_text
```


---

### Create embeddings {#create-embeddings}

*Source: https://docs.twelvelabs.io/v1.3/docs/guides/create-embeddings*

##### Video embeddings


---

### Search {#search}

*Source: https://docs.twelvelabs.io/v1.3/docs/guides/search*

#### Import the SDK and initialize the client

Create a client instance to interact with the TwelveLabs Video Understanding platform. Function call: You call the constructor of the TwelveLabs class. Parameters:

- api_key: The API key to authenticate your requests to the platform.

Return value: An object of type TwelveLabs configured for making API calls.

#### Specify the index containing your videos

Indexes help you organize and search through related videos efficiently. This example creates a new index, but you can also use an existing index by specifying its unique identifier. See the Indexes page for more details on creating an index. Function call: You call the index.create function. Parameters:

- name: The name of the index.
- models: An object specifying your model configuration. This example enables the Marengo video understanding model and the visual and audio model options.

Return value: An object containing, among other information, a field named id representing the unique identifier of the newly created index.

#### Upload videos

To perform any downstream tasks, you must first upload your videos, and the platform must finish processing them. Function call: You call the task.create function. This starts a video indexing task, which is an object of type Task that tracks the status of your video upload and indexing process. Parameters:

- index_id: The unique identifier of your index.
- file or url: The path or the publicly accessible URL of your video file.

Return value: An object of type Task containing, among other information, the following fields:

- video_id: The unique identifier of your video
- status: The status of your video indexing task.

#### Monitor the indexing process

The platform requires some time to index videos. Check the status of the video indexing task until it’s completed. Function call: You call the task.wait_for_done function. Parameters:

- sleep_interval: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
- callback: A callback function that the SDK executes each time it checks the status. Note that the callback function takes a parameter of type Task representig the video indexing task you’ve created in the previous step. Use it to display the status of your video indexing task.

Return value: An object containing, among other information, a field named status representing the status of your task. Wait until the value of this field is ready.

#### Perform a search request

Perform a search within your index using a text or image query.

#### Process the search results

Display the search results, including handling pagination to retrieve all pages. Function call: Iterate over the results by calling the next function. Parameters: The search results retrieved in the previous step.

Return value: The next page or raises a StopIteration exception if the iterator has reached the last page.

##### Search with text and image queries

#### Code Examples

```plaintext
$pip install twelvelabs
```

```plaintext
$pip install twelvelabs
```

```plaintext
<>
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# 1. Initialize the client5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# 2. Create an index8models = [ {"name": "marengo2.7", "options": ["visual", "audio"]}]9index = client.index.create(name="<YOUR_INDEX_NAME>", models=models)10print(f"Index created: id={index.id}, name={index.name}")1112# 3. Upload a video13task = client.task.create(index_id=index.id, file="<YOUR_VIDEO_FILE>")14print(f"Task id={task.id}, Video id={task.video_id}")1516# 4. Monitor the indexing process17def on_task_update(task: Task):18print(f"  Status={task.status}")19task.wait_for_done(sleep_interval=5, callback=on_task_update)20if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")2324# 5. Perform a search request25search_results = client.search.query(26index_id=index.id,  query_text="<YOUR_QUERY>", options=["visual", "audio"], operator="or")2728# 6. Process the search results29def print_page(page):30for clip in page:31print(32f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"33)34print_page(search_results.data)35while True:36try:37print_page(next(search_results))38except StopIteration:39break
```

```plaintext
TwelveLabs
```

```plaintext
api_key
```

```plaintext
TwelveLabs
```

```plaintext
index.create
```

```plaintext
name
```

```plaintext
models
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
id
```

```plaintext
task.create
```

```plaintext
Task
```

```plaintext
index_id
```

```plaintext
file
```

```plaintext
url
```

```plaintext
Task
```

```plaintext
video_id
```

```plaintext
status
```

```plaintext
task.wait_for_done
```

```plaintext
sleep_interval
```

```plaintext
callback
```

```plaintext
Task
```

```plaintext
status
```

```plaintext
ready
```

```plaintext
search.query
```

```plaintext
index_id
```

```plaintext
query_text
```

```plaintext
options
```

```plaintext
operator
```

```plaintext
data
```

```plaintext
video_id
```

```plaintext
start
```

```plaintext
end
```

```plaintext
score
```

```plaintext
page_info
```

```plaintext
pool
```

```plaintext
next
```

```plaintext
StopIteration
```


---

## Concepts {#concepts}

### Models {#models}

*Source: https://docs.twelvelabs.io/docs/concepts*

##### Marengo


---

### Indexes {#indexes}

*Source: https://docs.twelvelabs.io/docs/concepts/indexes*

### Create an index

To create a new index, you must provide the following parameters:

- name: A string representing the name of your new index. Choose a succinct and descriptive name for your index.
- models: An object specifying your model configuration. You constructed this object in the previous step.
- (Optional) addons: An array of strings specifying the add-ons you want to enable for your index. This example enables the thumbnail generation feature.

The response should look similar to the following one:

Note that the response contains, among other information, a field named id, representing the unique identifier of your new index.

- API Reference > Manage indexes
- Pyton SDK Reference > Manage indexes
- Node.js SDK Reference > Manage indexes

##### Tasks

#### Code Examples

```plaintext
addons
```

```plaintext
thumbnail
```

```plaintext
name
```

```plaintext
models
```

```plaintext
addons
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5}6]7index = client.index.create(8name="<YOUR_INDEX_NAME>",9models=models,10addons=["thumbnail"] # Optional11)12print(f"A new index has been created: id={index.id} name={index.name} models={index.models}")
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5}6]7index = client.index.create(8name="<YOUR_INDEX_NAME>",9models=models,10addons=["thumbnail"] # Optional11)12print(f"A new index has been created: id={index.id} name={index.name} models={index.models}")
```

```plaintext
A new index has been created: id=65d345106efba5e3988d6d4b name=index-01 models=[Model(name='marengo2.7', options=['visual', 'audio'], addons=['thumbnail'])]
```

```plaintext
A new index has been created: id=65d345106efba5e3988d6d4b name=index-01 models=[Model(name='marengo2.7', options=['visual', 'audio'], addons=['thumbnail'])]
```

```plaintext
id
```


---

### Modalities {#modalities}

*Source: https://docs.twelvelabs.io/docs/concepts/modalities*

##### Multimodal large language models


---

### Models {#models}

*Source: https://docs.twelvelabs.io/docs/concepts/models#supported-languages*

##### Marengo


---

### Marengo {#marengo}

*Source: https://docs.twelvelabs.io/docs/concepts/models/marengo*

### Steve Jobs introducing the iPhone

In the example screenshot below, the query was “How did Steve Jobs introduce the iPhone?”. The Marengo video understanding model used information found in the visual and conversation modalities to perform the following tasks:

- Visual recognition of a famous person (Steve Jobs)
- Joint speech and visual recognition to semantically search for the moment when Steve Jobs introduced the iPhone. Note that semantic search finds information based on the intended meaning of the query rather than the literal words you used, meaning that the platform identified the matching video fragments even if Steve Jobs didn’t explicitly say the words in the query.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Polar bear holding a Coca-Cola bottle

In the example screenshot below, the query was “Polar bear holding a Coca-Cola bottle.” The Marengo video understanding model used information found in the visual and logo modalities to perform the following tasks:

- Recognition of a cartoon character (polar bear)
- Identification of an object (bottle)
- Detection of a specific brand logo (Coca-Cola)
- Identification of an action (polar bear holding a bottle)



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Using different languages

This section provides examples of using different languages to perform search requests.

#### Spanish

In the example screenshot below, the query was “¿Cómo presentó Steve Jobs el iPhone?” (“How did Steve Jobs introduce the iPhone?”). The Marengo video understanding model used information from the visual and audio modalities.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

#### Chinese

In the example screenshot below, the query was “猫做有趣的事情” (“Cats doing funny things.”). The Marengo video understanding model used information from the visual modality.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

#### French

In the example screenshot below, the query was “J’ai trouvé la solution” (“I found the solution.”). The Marengo video understanding model used information from the visual modality (text displayed on the screen).



For support or feedback regarding Marengo, contact support@twelvelabs.io.

##### Pegasus


---

### Multimodal large language models {#multimodal-large-language-models}

*Source: https://docs.twelvelabs.io/docs/concepts/multimodal-large-language-models*

##### Organizations


---

### Tasks {#tasks}

*Source: https://docs.twelvelabs.io/docs/concepts/tasks*

##### Modalities

#### Code Examples

```plaintext
validating
```

```plaintext
pending
```

```plaintext
queued
```

```plaintext
indexing
```

```plaintext
ready
```

```plaintext
failed
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# Initialize the TwelveLabs client with your API key5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# Upload a video file by creating a video indexing task8task = client.task.create(9index_id="<YOUR_INDEX_ID>",10file="<YOUR_VIDEO_FILE>"11)12print(f"Task id={task.id}")1314# Monitor the task status until the status is ready15def on_task_update(task: Task):16print(f"  Status={task.status}")1718task.wait_for_done(sleep_interval=5, callback=on_task_update)1920if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.task import Task34# Initialize the TwelveLabs client with your API key5client = TwelveLabs(api_key="<YOUR_API_KEY>")67# Upload a video file by creating a video indexing task8task = client.task.create(9index_id="<YOUR_INDEX_ID>",10file="<YOUR_VIDEO_FILE>"11)12print(f"Task id={task.id}")1314# Monitor the task status until the status is ready15def on_task_update(task: Task):16print(f"  Status={task.status}")1718task.wait_for_done(sleep_interval=5, callback=on_task_update)1920if task.status != "ready":21raise RuntimeError(f"Indexing failed with status {task.status}")22print(f"The unique identifier of your video is {task.video_id}.")
```

```plaintext
processing
```

```plaintext
ready
```

```plaintext
failed
```

```plaintext
1from twelvelabs import TwelveLabs2from typing import List3from twelvelabs.models.embed import EmbeddingsTask, SegmentEmbedding45# Initialize the TwelveLabs client with your API key6client = TwelveLabs(api_key="<YOUR_API_KEY>")78# Upload a video9task = client.embed.task.create(model_name="Marengo-retrieval-2.7", video_file="<YOUR_VIDEO_FILE>")10print(11f"Created task: id={task.id} model_name={task.model_name} status={task.status}")1213# Monitor the status14def on_task_update(task: EmbeddingsTask):15print(f"  Status={task.status}")16status = task.wait_for_done(sleep_interval=2, callback=on_task_update)17print(f"Embedding done: {status}")
```

```plaintext
1from twelvelabs import TwelveLabs2from typing import List3from twelvelabs.models.embed import EmbeddingsTask, SegmentEmbedding45# Initialize the TwelveLabs client with your API key6client = TwelveLabs(api_key="<YOUR_API_KEY>")78# Upload a video9task = client.embed.task.create(model_name="Marengo-retrieval-2.7", video_file="<YOUR_VIDEO_FILE>")10print(11f"Created task: id={task.id} model_name={task.model_name} status={task.status}")1213# Monitor the status14def on_task_update(task: EmbeddingsTask):15print(f"  Status={task.status}")16status = task.wait_for_done(sleep_interval=2, callback=on_task_update)17print(f"Embedding done: {status}")
```


---

### Indexes {#indexes}

*Source: https://docs.twelvelabs.io/v1.3/docs/concepts/indexes*

### Create an index

To create a new index, you must provide the following parameters:

- name: A string representing the name of your new index. Choose a succinct and descriptive name for your index.
- models: An object specifying your model configuration. You constructed this object in the previous step.
- (Optional) addons: An array of strings specifying the add-ons you want to enable for your index. This example enables the thumbnail generation feature.

The response should look similar to the following one:

Note that the response contains, among other information, a field named id, representing the unique identifier of your new index.

- API Reference > Manage indexes
- Pyton SDK Reference > Manage indexes
- Node.js SDK Reference > Manage indexes

##### Tasks

#### Code Examples

```plaintext
addons
```

```plaintext
thumbnail
```

```plaintext
name
```

```plaintext
models
```

```plaintext
addons
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5}6]7index = client.index.create(8name="<YOUR_INDEX_NAME>",9models=models,10addons=["thumbnail"] # Optional11)12print(f"A new index has been created: id={index.id} name={index.name} models={index.models}")
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5}6]7index = client.index.create(8name="<YOUR_INDEX_NAME>",9models=models,10addons=["thumbnail"] # Optional11)12print(f"A new index has been created: id={index.id} name={index.name} models={index.models}")
```

```plaintext
A new index has been created: id=65d345106efba5e3988d6d4b name=index-01 models=[Model(name='marengo2.7', options=['visual', 'audio'], addons=['thumbnail'])]
```

```plaintext
A new index has been created: id=65d345106efba5e3988d6d4b name=index-01 models=[Model(name='marengo2.7', options=['visual', 'audio'], addons=['thumbnail'])]
```

```plaintext
id
```


---

### Modalities {#modalities}

*Source: https://docs.twelvelabs.io/v1.3/docs/concepts/modalities#model-options*

##### Multimodal large language models


---

### Models {#models}

*Source: https://docs.twelvelabs.io/v1.3/docs/concepts/models*

##### Marengo


---

### Marengo {#marengo}

*Source: https://docs.twelvelabs.io/v1.3/docs/concepts/models/marengo*

### Steve Jobs introducing the iPhone

In the example screenshot below, the query was “How did Steve Jobs introduce the iPhone?”. The Marengo video understanding model used information found in the visual and conversation modalities to perform the following tasks:

- Visual recognition of a famous person (Steve Jobs)
- Joint speech and visual recognition to semantically search for the moment when Steve Jobs introduced the iPhone. Note that semantic search finds information based on the intended meaning of the query rather than the literal words you used, meaning that the platform identified the matching video fragments even if Steve Jobs didn’t explicitly say the words in the query.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Polar bear holding a Coca-Cola bottle

In the example screenshot below, the query was “Polar bear holding a Coca-Cola bottle.” The Marengo video understanding model used information found in the visual and logo modalities to perform the following tasks:

- Recognition of a cartoon character (polar bear)
- Identification of an object (bottle)
- Detection of a specific brand logo (Coca-Cola)
- Identification of an action (polar bear holding a bottle)



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Using different languages

This section provides examples of using different languages to perform search requests.

#### Spanish

In the example screenshot below, the query was “¿Cómo presentó Steve Jobs el iPhone?” (“How did Steve Jobs introduce the iPhone?”). The Marengo video understanding model used information from the visual and audio modalities.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

#### Chinese

In the example screenshot below, the query was “猫做有趣的事情” (“Cats doing funny things.”). The Marengo video understanding model used information from the visual modality.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

#### French

In the example screenshot below, the query was “J’ai trouvé la solution” (“I found the solution.”). The Marengo video understanding model used information from the visual modality (text displayed on the screen).



For support or feedback regarding Marengo, contact support@twelvelabs.io.

##### Pegasus


---

### Pegasus {#pegasus}

*Source: https://docs.twelvelabs.io/v1.3/docs/concepts/models/pegasus*

### Summarizing educational videos

In the example screenshot below, the platform has summarized an educational video using predefined templates without any customization:



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Generating captions for social media

In the example screenshot below, the prompt instructs the platform to generate a caption for a social media post:



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Writing police reports

In the example screenshot below, the prompt instructs the platform to write a police report using a specific template for a video showing a robbery:



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

### Using different languages

This sections provides example of using different languages to generate text from videos.

#### Spanish

The following example summarizes a video, indicating that the response should be in Spanish. Note that the prompt is in English, and the output is in Spanish.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

#### French

The following example summarizes the main three takeaways from this video. Note that the prompt and the output are in French.



To see this example in the Playground, ensure you’re logged in, and then open this URL in your browser.

For support or feedback regarding Pegasus, contact support@twelvelabs.io.

##### Indexes


---

## API Reference {#api-reference}

### Analyze videos {#analyze-videos}

*Source: https://docs.twelvelabs.io/api-reference/analyze-videos*

##### Titles, topics, or hashtags

#### Code Examples

```plaintext
/gist
```

```plaintext
/summarize
```

```plaintext
/analyze
```


---

### Open-ended analysis {#open-ended-analysis}

*Source: https://docs.twelvelabs.io/api-reference/analyze-videos/analyze*

#### Headers

#### Request

#### Response

#### Errors

##### Error codes

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/analyze \2-H "x-api-key: <apiKey>" \3-H "Content-Type: application/json" \4-d '{5"video_id": "6298d673f1090f1100476d4c",6"prompt": "I want to generate a description for my video with the following format - Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks.",7"temperature": 0.2,8"stream": true9}'
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/analyze \2-H "x-api-key: <apiKey>" \3-H "Content-Type: application/json" \4-d '{5"video_id": "6298d673f1090f1100476d4c",6"prompt": "I want to generate a description for my video with the following format - Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks.",7"temperature": 0.2,8"stream": true9}'
```

```plaintext
1{}
```

```plaintext
1{}
```

```plaintext
true
```

```plaintext
true
```

```plaintext
true
```


---

### Summaries, chapters, or highlights {#summaries-chapters-or-highlights}

*Source: https://docs.twelvelabs.io/api-reference/analyze-videos/summarize*

#### Headers

#### Request

#### Response

#### Errors

##### Open-ended texts

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/summarize \2-H "x-api-key: <apiKey>" \3-H "Content-Type: application/json" \4-d '{5"video_id": "6298d673f1090f1100476d4c",6"type": "summary",7"prompt": "Generate a summary of this video for a social media post, up to two sentences.",8"temperature": 0.29}'
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/summarize \2-H "x-api-key: <apiKey>" \3-H "Content-Type: application/json" \4-d '{5"video_id": "6298d673f1090f1100476d4c",6"type": "summary",7"prompt": "Generate a summary of this video for a social media post, up to two sentences.",8"temperature": 0.29}'
```

```plaintext
1{2"id": "663da73b31cdd0c1f638a8e6",3"usage": {4"output_tokens": 1005}6}
```

```plaintext
1{2"id": "663da73b31cdd0c1f638a8e6",3"usage": {4"output_tokens": 1005}6}
```

```plaintext
summary
```

```plaintext
chapter
```

```plaintext
highlight
```

```plaintext
type
```

```plaintext
summary
```

```plaintext
type
```

```plaintext
chapter
```

```plaintext
type
```

```plaintext
highlight
```


---

### Any-to-video search {#any-to-video-search}

*Source: https://docs.twelvelabs.io/api-reference/any-to-video-search*

##### Make any-to-video search requests


---

### Authentication {#authentication}

*Source: https://docs.twelvelabs.io/api-reference/authentication*

##### Typical workflows

#### Code Examples

```plaintext
requests
```

```plaintext
$python -m pip install requests
```

```plaintext
$python -m pip install requests
```

```plaintext
1import requests23# Step 2: Define the API URL and the specific endpoint4API_URL = "https://api.twelvelabs.io/v1.3"5INDEXES_URL = f"{API_URL}/indexes"67# Step 3: Create the necessary headers for authentication8headers = {9"x-api-key": "<YOUR_API_KEY>"10}1112# Step 4: Prepare the data payload for your API request13INDEX_NAME = "<YOUR_INDEX_NAME>"14data = {15"models": [16{17"model_name": "marengo2.7",18"model_options": ["visual", "audio"]19}20],21"index_name": INDEX_NAME22}2324# Step 5: Send the API request and process the response25response = requests.post(INDEXES_URL, headers=headers, json=data)26print(f"Status code: {response.status_code}")27if response.status_code == 201:28print(response.json())29else:30print("Error:", response.json())
```

```plaintext
1import requests23# Step 2: Define the API URL and the specific endpoint4API_URL = "https://api.twelvelabs.io/v1.3"5INDEXES_URL = f"{API_URL}/indexes"67# Step 3: Create the necessary headers for authentication8headers = {9"x-api-key": "<YOUR_API_KEY>"10}1112# Step 4: Prepare the data payload for your API request13INDEX_NAME = "<YOUR_INDEX_NAME>"14data = {15"models": [16{17"model_name": "marengo2.7",18"model_options": ["visual", "audio"]19}20],21"index_name": INDEX_NAME22}2324# Step 5: Send the API request and process the response25response = requests.post(INDEXES_URL, headers=headers, json=data)26print(f"Status code: {response.status_code}")27if response.status_code == 201:28print(response.json())29else:30print("Error:", response.json())
```


---

### Error codes {#error-codes}

*Source: https://docs.twelvelabs.io/api-reference/error-codes*

#### Code Examples

```plaintext
parameter_invalid
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
parameter_not_provided
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
parameter_unknown
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
resource_not_exist
```

```plaintext
{resource_id}
```

```plaintext
{collection_name}
```

```plaintext
api_key_invalid
```

```plaintext
tags_not_allowed
```

```plaintext
{tag}
```

```plaintext
{tags}
```

```plaintext
api_upgrade_required
```

```plaintext
{version}
```

```plaintext
{current_version}
```

```plaintext
/indexes
```

```plaintext
index_option_cannot_be_changed
```

```plaintext
index_engine_cannot_be_changed
```

```plaintext
index_name_already_exists
```

```plaintext
{index_name}
```

```plaintext
/tasks
```

```plaintext
video_resolution_too_low
```

```plaintext
{current_resolution}
```

```plaintext
video_resolution_too_high
```

```plaintext
{current_resolution}
```

```plaintext
video_resolution_invalid_aspect_ratio
```

```plaintext
{current_resolution}
```

```plaintext
video_duration_too_short
```

```plaintext
{current_duration}
```

```plaintext
video_duration_too_long
```

```plaintext
{current_duration}
```

```plaintext
video_file_broken
```

```plaintext
task_cannot_be_deleted
```

```plaintext
usage_limit_exceeded
```

```plaintext
video_filesize_too_large
```

```plaintext
{maximum_size}
```

```plaintext
{current_file_size}
```

```plaintext
/search
```

```plaintext
search_option_not_supported
```

```plaintext
{search_option}
```

```plaintext
{index_id}
```

```plaintext
{supported_search_option}
```

```plaintext
search_option_combination_not_supported
```

```plaintext
{search_option}
```

```plaintext
{other_combination}
```

```plaintext
search_filter_invalid
```

```plaintext
search_page_token_expired
```

```plaintext
{next_page_token}
```

```plaintext
index_not_supported_for_search
```

```plaintext
/generate
```

```plaintext
token_limit_exceeded
```

```plaintext
index_not_supported_for_generate
```

```plaintext
/summarize
```

```plaintext
token_limit_exceeded
```

```plaintext
/embed
```

```plaintext
parameter_invalid
```

```plaintext
text
```

```plaintext
text_truncate
```

```plaintext
none
```

```plaintext
start
```

```plaintext
end
```

```plaintext
/embed/tasks
```

```plaintext
parameter_invalid
```

```plaintext
video_clip_length
```

```plaintext
video_clip_length
```

```plaintext
video_end_offset_sec
```

```plaintext
video_end_offset_sec
```

```plaintext
video_start_offset_sec
```

```plaintext
/embed/tasks/{task-id}/status
```

```plaintext
parameter_invalid
```

```plaintext
task_id
```

```plaintext
task_id
```


---

### Manage indexes {#manage-indexes}

*Source: https://docs.twelvelabs.io/api-reference/indexes*

##### The index object


---

### Introduction {#introduction}

*Source: https://docs.twelvelabs.io/api-reference/introduction#errors*

### HTTP status codes

The following list is a summary of the HTTP status codes returned by the API:

- 200: The request was successful.
- 201: The request was successful and a new resource was created.
- 400: The API service cannot process the request. See the code and message fields in the response for more details about the error.
- 401: The API key you provided is not valid. Note that, for security reasons, your API key automatically expires every two months. When your key has expired, you must generate a new one to continue using the API.
- 404: The requested resource was not found.
- 429: Indicates that a rate limit has been reached.

### Errors

HTTP status codes in the 4xx range indicate an error caused by the parameters you provided in the request. For each error, the API service returns the following fields in the body of the response:

- code: A string representing the error code.
- message: A human-readable string describing the error, intended to be suitable for display in a user interface.
- (Optional) docs_url: The URL of the relevant documentation page.

For more details, see the Error codes page.

##### Authentication

#### Code Examples

```plaintext
{Method} {BaseURL}/{version}/{resource}/{path_parameters}?{query_parameters}
```

```plaintext
GET
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
DELETE
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
https://api.twelvelabs.io
```

```plaintext
v1.3
```

```plaintext
X-Api-Version
```

```plaintext
200
```

```plaintext
201
```

```plaintext
400
```

```plaintext
code
```

```plaintext
message
```

```plaintext
401
```

```plaintext
404
```

```plaintext
429
```

```plaintext
4xx
```

```plaintext
code
```

```plaintext
message
```

```plaintext
docs_url
```


---

### Upload videos {#upload-videos}

*Source: https://docs.twelvelabs.io/api-reference/tasks*

##### The task object


---

### Create text, image, and audio embeddings {#create-text-image-and-audio-embeddings}

*Source: https://docs.twelvelabs.io/api-reference/text-image-audio-embeddings*

##### The embedding object


---

### Typical workflows {#typical-workflows}

*Source: https://docs.twelvelabs.io/api-reference/typical-workflows*

##### Manage indexes


---

### Create video embeddings {#create-video-embeddings}

*Source: https://docs.twelvelabs.io/api-reference/video-embeddings*

##### The video embedding object


---

### Manage videos {#manage-videos}

*Source: https://docs.twelvelabs.io/api-reference/videos*

##### The video object


---

### Retrieve video information {#retrieve-video-information}

*Source: https://docs.twelvelabs.io/api-reference/videos/retrieve*

#### Path parameters

#### Headers

#### Query parameters

#### Response

#### Errors

##### Update video information

#### Code Examples

```plaintext
1curl -G https://api.twelvelabs.io/v1.3/indexes/6298d673f1090f1100476d4c/videos/6298d673f1090f1100476d4c \2-H "x-api-key: <apiKey>" \3-d transcription=true
```

```plaintext
1curl -G https://api.twelvelabs.io/v1.3/indexes/6298d673f1090f1100476d4c/videos/6298d673f1090f1100476d4c \2-H "x-api-key: <apiKey>" \3-d transcription=true
```

```plaintext
1{2"_id": "61e17be5777e6caec646fa07",3"created_at": "2022-01-14T13:34:29Z",4"updated_at": "2022-01-14T13:34:29Z",5"indexed_at": "2022-01-14T14:05:55Z",6"system_metadata": {7"duration": 3747.841667,8"filename": "IOKgzkakhlk.mp4",9"fps": 29.97002997002997,10"height": 360,11"width": 48212},13"user_metadata": {14"category": "recentlyAdded",15"batchNumber": 5,16"rating": 9.3,17"needsReview": true18},19"hls": {20"video_url": "https://d2cp8xx7n5vxnu.cloudfront.net/6298aa0b535db125bf6e1d10/64902a28fb01304dd47be3cb/stream/c924f34a-144e-41df-bf2a-c693703fa134.m3u8",21"thumbnail_urls": [22"https://d2cp8xx7n5vxnu.cloudfront.net/6298aa0b535db125bf6e1d10/64902a28fb01304dd47be3cb/thumbnails/c924f34a-144e-41df-bf2a-c693703fa134.0000001.jpg"23],24"status": "COMPLETE",25"updated_at": "2024-01-16T07:59:40.879Z"26},27"embedding": {28"model_name": "Marengo-retrieval-2.7",29"video_embedding": {30"segments": [31{32"embedding_option": "visual-text",33"embedding_scope": "clip",34"end_offset_sec": 7.5666666,35"float": [36-0.04747168,370.030509098,380.03228246839],40"start_offset_sec": 041}42]43}44},45"transcription": [46{47"start": 0,48"end": 10.5,49"value": "Hello, how are you?"50},51{52"start": 10.5,53"end": 15.2,54"value": "I'm fine, thank you."55}56]57}
```

```plaintext
1{2"_id": "61e17be5777e6caec646fa07",3"created_at": "2022-01-14T13:34:29Z",4"updated_at": "2022-01-14T13:34:29Z",5"indexed_at": "2022-01-14T14:05:55Z",6"system_metadata": {7"duration": 3747.841667,8"filename": "IOKgzkakhlk.mp4",9"fps": 29.97002997002997,10"height": 360,11"width": 48212},13"user_metadata": {14"category": "recentlyAdded",15"batchNumber": 5,16"rating": 9.3,17"needsReview": true18},19"hls": {20"video_url": "https://d2cp8xx7n5vxnu.cloudfront.net/6298aa0b535db125bf6e1d10/64902a28fb01304dd47be3cb/stream/c924f34a-144e-41df-bf2a-c693703fa134.m3u8",21"thumbnail_urls": [22"https://d2cp8xx7n5vxnu.cloudfront.net/6298aa0b535db125bf6e1d10/64902a28fb01304dd47be3cb/thumbnails/c924f34a-144e-41df-bf2a-c693703fa134.0000001.jpg"23],24"status": "COMPLETE",25"updated_at": "2024-01-16T07:59:40.879Z"26},27"embedding": {28"model_name": "Marengo-retrieval-2.7",29"video_embedding": {30"segments": [31{32"embedding_option": "visual-text",33"embedding_scope": "clip",34"end_offset_sec": 7.5666666,35"float": [36-0.04747168,370.030509098,380.03228246839],40"start_offset_sec": 041}42]43}44},45"transcription": [46{47"start": 0,48"end": 10.5,49"value": "Hello, how are you?"50},51{52"start": 10.5,53"end": 15.2,54"value": "I'm fine, thank you."55}56]57}
```

```plaintext
visual-text
```

```plaintext
audio
```

```plaintext
embedding_option
```

```plaintext
model_options
```

```plaintext
model_options
```

```plaintext
visual,
```

```plaintext
embedding_option
```

```plaintext
audio
```

```plaintext
visual-text
```

```plaintext
audio
```

```plaintext
enable_video_stream
```

```plaintext
true
```

```plaintext
embedding_option
```

```plaintext
data
```

```plaintext
null
```


---

### Introduction {#introduction}

*Source: https://docs.twelvelabs.io/reference/api-reference*

### HTTP status codes

The following list is a summary of the HTTP status codes returned by the API:

- 200: The request was successful.
- 201: The request was successful and a new resource was created.
- 400: The API service cannot process the request. See the code and message fields in the response for more details about the error.
- 401: The API key you provided is not valid. Note that, for security reasons, your API key automatically expires every two months. When your key has expired, you must generate a new one to continue using the API.
- 404: The requested resource was not found.
- 429: Indicates that a rate limit has been reached.

### Errors

HTTP status codes in the 4xx range indicate an error caused by the parameters you provided in the request. For each error, the API service returns the following fields in the body of the response:

- code: A string representing the error code.
- message: A human-readable string describing the error, intended to be suitable for display in a user interface.
- (Optional) docs_url: The URL of the relevant documentation page.

For more details, see the Error codes page.

##### Authentication

#### Code Examples

```plaintext
{Method} {BaseURL}/{version}/{resource}/{path_parameters}?{query_parameters}
```

```plaintext
GET
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
DELETE
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
https://api.twelvelabs.io
```

```plaintext
v1.3
```

```plaintext
X-Api-Version
```

```plaintext
200
```

```plaintext
201
```

```plaintext
400
```

```plaintext
code
```

```plaintext
message
```

```plaintext
401
```

```plaintext
404
```

```plaintext
429
```

```plaintext
4xx
```

```plaintext
code
```

```plaintext
message
```

```plaintext
docs_url
```


---

### Make any-to-video search requests {#make-any-to-video-search-requests}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/any-to-video-search/make-search-request*

#### Headers

#### Request

#### Response

#### Errors

##### Retrieve a specific page of search results

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/search \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F query_media_file=@<file1> \5-F query_text="A man walking a dog" \6-F index_id="6298d673f1090f1100476d4c" \7-F search_options='[8"visual"9]' \10-F adjust_confidence_level='0.5' \11-F group_by="clip" \12-F sort_option="score" \13-F operator="or" \14-F page_limit='10' \15-F filter="{\"id\":[\"66284191ea717fa66a274832\"]}"
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/search \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F query_media_file=@<file1> \5-F query_text="A man walking a dog" \6-F index_id="6298d673f1090f1100476d4c" \7-F search_options='[8"visual"9]' \10-F adjust_confidence_level='0.5' \11-F group_by="clip" \12-F sort_option="score" \13-F operator="or" \14-F page_limit='10' \15-F filter="{\"id\":[\"66284191ea717fa66a274832\"]}"
```

```plaintext
1{2"data": [3{4"score": 85.08,5"start": 238.75,6"end": 259.62109375,7"video_id": "639963a1ce36463e0199c8c7",8"confidence": "high",9"thumbnail_url": "https://example.com/thumbnail.jpg",10"transcription": "A woman vlogs about her summer day, sharing her experience"11}12],13"search_pool": {14"total_count": 10,15"total_duration": 8731,16"index_id": "639961c9e219c90227c371a2"17}18}
```

```plaintext
1{2"data": [3{4"score": 85.08,5"start": 238.75,6"end": 259.62109375,7"video_id": "639963a1ce36463e0199c8c7",8"confidence": "high",9"thumbnail_url": "https://example.com/thumbnail.jpg",10"transcription": "A woman vlogs about her summer day, sharing her experience"11}12],13"search_pool": {14"total_count": 10,15"total_duration": 8731,16"index_id": "639961c9e219c90227c371a2"17}18}
```

```plaintext
query_text
```

```plaintext
query_media_type
```

```plaintext
image
```

```plaintext
query_media_url
```

```plaintext
query_media_file
```

```plaintext
query_media_url
```

```plaintext
query_media_file
```

```plaintext
query_media_url
```

```plaintext
image
```

```plaintext
query_media_file
```

```plaintext
query_media_url
```

```plaintext
search_options
```

```plaintext
operator
```

```plaintext
1--form search_options=visual \2--form search_options=audio \
```

```plaintext
1--form search_options=visual \2--form search_options=audio \
```

```plaintext
clip
```

```plaintext
video
```

```plaintext
clip
```

```plaintext
clip
```

```plaintext
low
```

```plaintext
low
```

```plaintext
score
```

```plaintext
score
```

```plaintext
group_by
```

```plaintext
video
```

```plaintext
score
```

```plaintext
clip_count
```

```plaintext
group_by
```

```plaintext
video
```

```plaintext
clip_count
```

```plaintext
score
```

```plaintext
or
```

```plaintext
or
```

```plaintext
and
```

```plaintext
or
```

```plaintext
10
```

```plaintext
50
```

```plaintext
=
```

```plaintext
{"field": "value"}
```

```plaintext
=
```

```plaintext
id
```

```plaintext
{"id": ["value1", "value2"]}
```

```plaintext
=
```

```plaintext
lte
```

```plaintext
gte
```

```plaintext
{"field": number}
```

```plaintext
{"field": { "gte": number, "lte": number }}
```

```plaintext
=
```

```plaintext
{"field": true}
```

```plaintext
{"field": false}
```

```plaintext
id
```

```plaintext
{"id": ["67cec9caf45d9b64a58340fc", "67cec9baf45d9b64a58340fa"]}
```

```plaintext
duration
```

```plaintext
gte
```

```plaintext
lte
```

```plaintext
{"duration": 600}
```

```plaintext
{"duration": { "gte": 600, "lte": 800 }}
```

```plaintext
width
```

```plaintext
gte
```

```plaintext
lte
```

```plaintext
{"width": 1920}
```

```plaintext
{"width": { "gte": 1280, "lte": 1920}}
```

```plaintext
height
```

```plaintext
gte
```

```plaintext
lte
```

```plaintext
{"height": 1080}
```

```plaintext
{"height": { "gte": 720, "lte": 1080 }}
```

```plaintext
size
```

```plaintext
gte
```

```plaintext
lte
```

```plaintext
{"size": 1048576}
```

```plaintext
{"size": { "gte": 1048576, "lte": 5242880}}
```

```plaintext
filename
```

```plaintext
{"filename": "Animal Encounters part 1"}
```

```plaintext
PUT
```

```plaintext
/indexes/:index-id/videos/:video-id
```

```plaintext
needsReview
```

```plaintext
true
```

```plaintext
{"needs_review": true}
```


---

### Error codes {#error-codes}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/error-codes*

#### Code Examples

```plaintext
parameter_invalid
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
parameter_not_provided
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
parameter_unknown
```

```plaintext
{parameter}
```

```plaintext
{parameters}
```

```plaintext
resource_not_exist
```

```plaintext
{resource_id}
```

```plaintext
{collection_name}
```

```plaintext
api_key_invalid
```

```plaintext
tags_not_allowed
```

```plaintext
{tag}
```

```plaintext
{tags}
```

```plaintext
api_upgrade_required
```

```plaintext
{version}
```

```plaintext
{current_version}
```

```plaintext
/indexes
```

```plaintext
index_option_cannot_be_changed
```

```plaintext
index_engine_cannot_be_changed
```

```plaintext
index_name_already_exists
```

```plaintext
{index_name}
```

```plaintext
/tasks
```

```plaintext
video_resolution_too_low
```

```plaintext
{current_resolution}
```

```plaintext
video_resolution_too_high
```

```plaintext
{current_resolution}
```

```plaintext
video_resolution_invalid_aspect_ratio
```

```plaintext
{current_resolution}
```

```plaintext
video_duration_too_short
```

```plaintext
{current_duration}
```

```plaintext
video_duration_too_long
```

```plaintext
{current_duration}
```

```plaintext
video_file_broken
```

```plaintext
task_cannot_be_deleted
```

```plaintext
usage_limit_exceeded
```

```plaintext
video_filesize_too_large
```

```plaintext
{maximum_size}
```

```plaintext
{current_file_size}
```

```plaintext
/search
```

```plaintext
search_option_not_supported
```

```plaintext
{search_option}
```

```plaintext
{index_id}
```

```plaintext
{supported_search_option}
```

```plaintext
search_option_combination_not_supported
```

```plaintext
{search_option}
```

```plaintext
{other_combination}
```

```plaintext
search_filter_invalid
```

```plaintext
search_page_token_expired
```

```plaintext
{next_page_token}
```

```plaintext
index_not_supported_for_search
```

```plaintext
/generate
```

```plaintext
token_limit_exceeded
```

```plaintext
index_not_supported_for_generate
```

```plaintext
/summarize
```

```plaintext
token_limit_exceeded
```

```plaintext
/embed
```

```plaintext
parameter_invalid
```

```plaintext
text
```

```plaintext
text_truncate
```

```plaintext
none
```

```plaintext
start
```

```plaintext
end
```

```plaintext
/embed/tasks
```

```plaintext
parameter_invalid
```

```plaintext
video_clip_length
```

```plaintext
video_clip_length
```

```plaintext
video_end_offset_sec
```

```plaintext
video_end_offset_sec
```

```plaintext
video_start_offset_sec
```

```plaintext
/embed/tasks/{task-id}/status
```

```plaintext
parameter_invalid
```

```plaintext
task_id
```

```plaintext
task_id
```


---

### Introduction {#introduction}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/introduction*

### HTTP status codes

The following list is a summary of the HTTP status codes returned by the API:

- 200: The request was successful.
- 201: The request was successful and a new resource was created.
- 400: The API service cannot process the request. See the code and message fields in the response for more details about the error.
- 401: The API key you provided is not valid. Note that, for security reasons, your API key automatically expires every two months. When your key has expired, you must generate a new one to continue using the API.
- 404: The requested resource was not found.
- 429: Indicates that a rate limit has been reached.

### Errors

HTTP status codes in the 4xx range indicate an error caused by the parameters you provided in the request. For each error, the API service returns the following fields in the body of the response:

- code: A string representing the error code.
- message: A human-readable string describing the error, intended to be suitable for display in a user interface.
- (Optional) docs_url: The URL of the relevant documentation page.

For more details, see the Error codes page.

##### Authentication

#### Code Examples

```plaintext
{Method} {BaseURL}/{version}/{resource}/{path_parameters}?{query_parameters}
```

```plaintext
GET
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
DELETE
```

```plaintext
POST
```

```plaintext
PUT
```

```plaintext
https://api.twelvelabs.io
```

```plaintext
v1.3
```

```plaintext
X-Api-Version
```

```plaintext
200
```

```plaintext
201
```

```plaintext
400
```

```plaintext
code
```

```plaintext
message
```

```plaintext
401
```

```plaintext
404
```

```plaintext
429
```

```plaintext
4xx
```

```plaintext
code
```

```plaintext
message
```

```plaintext
docs_url
```


---

### Create a video indexing task {#create-a-video-indexing-task}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/tasks/create*

#### Headers

#### Request

#### Response

#### Errors

##### List video indexing tasks

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/tasks \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F index_id="6298d673f1090f1100476d4c" \5-F video_file=@@/Users/john/Documents/01.mp4
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/tasks \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F index_id="6298d673f1090f1100476d4c" \5-F video_file=@@/Users/john/Documents/01.mp4
```

```plaintext
1{2"_id": "62a1ec6d9ea24f052b971a0f",3"video_id": "62a1ec6d9ea24f052b971a0f"4}
```

```plaintext
1{2"_id": "62a1ec6d9ea24f052b971a0f",3"video_id": "62a1ec6d9ea24f052b971a0f"4}
```

```plaintext
video_file
```

```plaintext
video_url
```

```plaintext
true
```

```plaintext
true
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos/{video-id}
```


---

### Create embeddings for text, image, and audio {#create-embeddings-for-text-image-and-audio}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/text-image-audio-embeddings/create-text-image-audio-embeddings*

#### Headers

#### Request

#### Response

#### Errors

##### Analyze videos

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/embed \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F model_name="Marengo-retrieval-2.7" \5-F text="Man with a dog crossing the street" \6-F image_file=@<file1> \7-F audio_file=@<file1>
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/embed \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F model_name="Marengo-retrieval-2.7" \5-F text="Man with a dog crossing the street" \6-F image_file=@<file1> \7-F audio_file=@<file1>
```

```plaintext
1{2"model_name": "Marengo-retrieval-2.7",3"text_embedding": {4"segments": [5{6"float": [7-0.042632885,80.014312328,90.02920905510]11}12]13},14"image_embedding": {15"segments": [16{17"float": [18-0.042632885,190.014312328,200.02920905521]22}23],24"metadata": {25"input_filename": "01.jpg"26}27},28"audio_embedding": {29"segments": [30{31"float": [32-0.042632885,330.014312328,340.02920905535],36"start_offset_sec": 037}38],39"metadata": {40"input_filename": "01.mp3"41}42}43}
```

```plaintext
1{2"model_name": "Marengo-retrieval-2.7",3"text_embedding": {4"segments": [5{6"float": [7-0.042632885,80.014312328,90.02920905510]11}12]13},14"image_embedding": {15"segments": [16{17"float": [18-0.042632885,190.014312328,200.02920905521]22}23],24"metadata": {25"input_filename": "01.jpg"26}27},28"audio_embedding": {29"segments": [30{31"float": [32-0.042632885,330.014312328,340.02920905535],36"start_offset_sec": 037}38],39"metadata": {40"input_filename": "01.mp3"41}42}43}
```

```plaintext
model_name
```

```plaintext
text
```

```plaintext
image_url
```

```plaintext
image_file
```

```plaintext
audio_url
```

```plaintext
audio_file
```

```plaintext
Marengo-retrieval-2.7
```

```plaintext
text_truncate
```

```plaintext
end
```

```plaintext
start
```

```plaintext
end
```

```plaintext
none
```

```plaintext
end
```

```plaintext
format: "uri"
```

```plaintext
image_file
```

```plaintext
image_url
```

```plaintext
format: "uri"
```

```plaintext
audio_file
```

```plaintext
audio_url
```

```plaintext
0
```

```plaintext
0
```


---

### Create a video embedding task {#create-a-video-embedding-task}

*Source: https://docs.twelvelabs.io/v1.3/api-reference/video-embeddings/create-video-embedding-task*

#### Headers

#### Request

#### Response

#### Errors

##### List video embedding tasks

#### Code Examples

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/embed/tasks \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F model_name="Marengo-retrieval-2.7" \5-F video_file=@/Users/john/Documents/video.mp4 \6-F video_embedding_scope="clip"
```

```plaintext
1curl -X POST https://api.twelvelabs.io/v1.3/embed/tasks \2-H "x-api-key: <apiKey>" \3-H "Content-Type: multipart/form-data" \4-F model_name="Marengo-retrieval-2.7" \5-F video_file=@/Users/john/Documents/video.mp4 \6-F video_embedding_scope="clip"
```

```plaintext
video_file
```

```plaintext
video_url
```

```plaintext
video_url
```

```plaintext
Marengo-retrieval-2.7
```

```plaintext
clip
```

```plaintext
clip
```

```plaintext
video_clip_length
```

```plaintext
video_start_offset_sec
```

```plaintext
video_end_offset_sec
```

```plaintext
clip
```

```plaintext
video
```

```plaintext
1--form video_embedding_scope=clip \2--form video_embedding_scope=video
```

```plaintext
1--form video_embedding_scope=clip \2--form video_embedding_scope=video
```

```plaintext
clip
```

```plaintext
GET
```

```plaintext
/embed/tasks/{task_id}/status
```

```plaintext
GET
```

```plaintext
/embed/tasks/{task_id}
```


---

## Resources {#resources}

### Platform overview {#platform-overview}

*Source: https://docs.twelvelabs.io/docs/resources*

### Indexes

An index is a basic unit for organizing and storing video data consisting of video embeddings and metadata. Indexes facilitate information retrieval and processing.

### Video understanding models

A video understanding model consists of a family of deep neural networks built on top of our multimodal foundation model for video understanding, offering search and summarization capabilities. For each index, you must configure the models you want to enable. See the Video understanding models page for more details about the available models and their capabilities.

### Model options

The model options define the types of information that a specific model will process. Currently, the platform provides the following model options: visual and audio. For more details, see the Model options page.

### Query/Prompt Processing Engine

This component processes the following user inputs and returns the corresponding results to your application:

- Search queries
- Prompts for analyzing videos and generating text based on their content

##### Playground


---

### Frequently asked questions {#frequently-asked-questions}

*Source: https://docs.twelvelabs.io/docs/resources/frequently-asked-questions*

### How does your model handle temporal dimension within videos?

We utilize a technique known as Positional Encoding, which is employed within the Transformers architecture to convey information regarding the position of a sequence of tokens within the input data. In this case, the tokens refer to the key scenes within the video. This technique facilitates the integration of sequential information into our model while simultaneously preserving the parallel processing capability of self-attention within the Transformer architecture.

### What is the maximum size of videos that can be stored in one index?

The Developer plan can accommodate up to 10,000 hours of video (whether in a single index or a combination of all indexes). For larger volumes, our enterprise plan would be best suited. Please contact us for more information at sales@twelvelabs.io.

### How long does it take to index a video?

Indexing is typically completed in 30-40% of the duration of the video. However, indexing duration also depends on the number of concurrent indexing tasks, and delays can occur if too many indexing tasks are being processed simultaneously. If you’re on the Free plan, for faster indexing, consider upgrading to the Developer plan, which supports more concurrent tasks. We also offer a dedicated cloud deployment option for enterprise customers. Please contact us at sales@twelvelabs.io to discuss this option.

### Can your model recognize natural sounds in videos?

Yes, the model analyzes visual and audio information and learns the correlation between certain visual objects or situations with sounds frequently appearing together.

### Can your models recognize text from other languages?

Yes, the models support multiple languages. See the Supported languages page for details.

### How does your visual language model compare to other LLMs?

The platform utilizes a multimodal approach for video understanding. Instead of relying on textual input like traditional LLMs, the platform interprets visuals, sounds, and spoken words to deliver comprehensive and accurate results.

### Can I use TwelveLabs with my own LLM or with LangChain?

You can optionally integrate our video-to-text model (Pegasus) with your LLMs. We also provide an open-source project demonstrating the integration with LangChain. Find out more at twelvelabs-io/tl-jockey.

### How can I change my login method?

To change your login method (for example, from username/password to SSO or vice versa), contact our support team at support@twelvelabs.io to delete your current account, then create a new one with your preferred login method.

### Does my invoice include a detailed cost breakdown?

If you’re on the Developer plan, TwelveLabs provides invoices that include a detailed cost breakdown. You can view your invoice using one of the following methods:

- Email: Open your invoice sent via email, and select the View invoice and payment details button.
- Playground: Go to the Billing & plan page, log in to your account, scroll to the Billing History section, and select the PDF for your invoice.

If you’re on the Enterprise plan, TwelveLabs provides invoices without detailed cost breakdowns.

This section answers frequently asked questions related to the Embed API.

### When should I use the Embed API versus the built-in search?

The Embed API and built-in search service offer different functionalities for working with visual content.

Embed API

- Generate visual embeddings for: RAG workflows Hybrid search Classification Clustering
- RAG workflows
- Hybrid search
- Classification
- Clustering
- Use the embeddings as input for your custom models
- Create flexible, domain-specific solutions

Built-in search service

- Perform semantic searches across multiple modalities: Visual content Conversation (human speech) Text-in-video (OCR) Logo
- Visual content
- Conversation (human speech)
- Text-in-video (OCR)
- Logo
- Utilize production-ready, out-of-the-box functionality
- Ideal for projects not requiring additional customization

This section answers frequently asked questions related to the Analyze API.

### What LLM does the Analyze API use?

The Analyze API employs our foundational Visual Language Model (VLM), which integrates a language encoder to extract multimodal data from videos and a decoder to generate concise text representations.

### To use the Analyze API, do I need to reindex my videos if I already indexed them with Marengo?

Yes, you must reindex videos using the Pegasus engine. See the Analyze videos and Pricing pages for details.

##### Sample applications


---

### From the community {#from-the-community}

*Source: https://docs.twelvelabs.io/docs/resources/from-the-community*

##### E-learning


---

### Migration guide {#migration-guide}

*Source: https://docs.twelvelabs.io/docs/resources/migration-guide*

### Global changes

### Deprecated endpoints

### Upload videos

### Manage indexes

### Manage videos

### Search

### Generate text from video

These changes add new functionality while maintaining backward compatibility.

### Upload videos

Migrating to v1.3 involves two main steps:

- Update your integration
- Update your code. Refer to the Migration Examples setion for details.

### 1. Update your integration

Choose the appropriate method based on how you interact with the TwelveLabs API:

- Official SDKs: Install version 0.4.x or later.
- HTTP client: Update your base URL.

### 2. Migration examples

Below are examples showing how to update your code for key breaking changes. Choose the examples matching your integration type.

#### Create indexes

Creating an index in version 1.3 includes the following key changes:

- Renamed parameters: The parameters that previously began with engine* have now been renamed to model*.
- Simplified modalities: The previous modalities of [visual, conversation, text_in_video, logo] have been simplified to [visual, audio].
- Marengo version update: Use “marengo2.7” instead of “marengo2.6”.

#### Perform a search request

Performing a search request includes the following key changes:

- Simplified modalities: The previous modalities of [visual, conversation, text_in_video, logo] have been simplified to [visual, audio].
- Deprecated parameter: The conversation_option parameter has been deprecated.
- Streamlined response: The metadata and modules fields in the response have been deprecated.

#### Create embeddings

Creating embeddings includes the following key changes:

- Marengo version update: Use “Marengo-retrieval-2.7” instead of “Marengo-retrieval-2.6”.
- Renamed parameter: The parameters that previously began with engine* have now been renamed to model*.

The following example creates a text embedding, but the principles demonstrated are similar for image, audio, and video embeddings:

#### Use Pegasus to classify videos

The Pegasus video understanding model offers flexible video classification through its text generation capabilities. You can use established category systems like YouTube video categories or IAB Tech Lab Content Taxonomy . You can also define custom categories for your specific needs.

The example below classifies a video based on YouTube’s video categories:

#### Detect logos

You can search for logos using text or image queries:

- Text queries: For logos that include text (example: Nike)
- Image queries: For logos without text (example: Apple’s apple symbol).

The following example searches for the Nike logo using a text query:

The following example searches for the Apple logo using an image query:

#### Search for text shown in videos

To search for text in videos, use text queries that target either on-screen text or spoken words in transcriptions rather than objects or concepts. The platform searches across both:

- Text shown on screen (such as titles, captions, or signs)
- Spoken words from audio transcriptions

Note that the platform may return both textual and visual matches. For example, searching for the word “smartphone” might return:

- Segments where “smartphone” appears as on-screen text.
- Segments where “smartphone” is spoken.
- Segments where smartphones are visible as objects.

The example below finds all the segments where the word “innovation” appears as on-screen text or as a spoken word in transcriptions:

#### Code Examples

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
engines
```

```plaintext
models
```

```plaintext
engine_name
```

```plaintext
model_name
```

```plaintext
engine_options
```

```plaintext
model_options
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation
```

```plaintext
audio
```

```plaintext
logo
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
text_in_video
```

```plaintext
/indexes
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
conversation
```

```plaintext
/search-v2
```

```plaintext
/search
```

```plaintext
/search
```

```plaintext
/classify
```

```plaintext
/engines
```

```plaintext
/engines/{engine-id}
```

```plaintext
/indexes/{index-id}/videos/{video-id}/text-in-video
```

```plaintext
/indexes/{index-id}/videos/{video-id}/logo
```

```plaintext
/indexes/{index_id}/videos/{video_id}/thumbnail
```

```plaintext
/indexes/{index-id}/videos/{video-id}/transcription
```

```plaintext
/search
```

```plaintext
/search/combined
```

```plaintext
/search
```

```plaintext
/search/combined
```

```plaintext
POST
```

```plaintext
/tasks
```

```plaintext
disable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
true
```

```plaintext
disable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
id
```

```plaintext
estimated_time
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}
```

```plaintext
_id
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos
```

```plaintext
metadata
```

```plaintext
user_metadata
```

```plaintext
user_metadata
```

```plaintext
metadata
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos
```

```plaintext
metadata
```

```plaintext
system_metadata
```

```plaintext
system_metadata
```

```plaintext
metadata
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos/{video-id}
```

```plaintext
metadata
```

```plaintext
system_metadata
```

```plaintext
system_metadata
```

```plaintext
metadata
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
conversation_option
```

```plaintext
conversation_option
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
GET
```

```plaintext
/search/{page-token}
```

```plaintext
page_info.page_expired_at
```

```plaintext
page_info.page_expires_at
```

```plaintext
page_expires_at
```

```plaintext
page_expired_at
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
GET
```

```plaintext
/search/{page-token}
```

```plaintext
metadata
```

```plaintext
modules
```

```plaintext
POST
```

```plaintext
/generate
```

```plaintext
stream
```

```plaintext
true
```

```plaintext
stream
```

```plaintext
false
```

```plaintext
POST
```

```plaintext
/tasks
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
GET
```

```plaintext
/tasks/{task-id
```

```plaintext
video_id
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
status
```

```plaintext
$pip3 install twelvelabs --upgrade
```

```plaintext
$pip3 install twelvelabs --upgrade
```

```plaintext
engine*
```

```plaintext
model*
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5},6{7"name": "pegasus1.2",8"options": ["visual", "audio"]9}10]11index = client.index.create(12name="<YOUR_INDEX_NAME>",13models=models,14addons=["thumbnail"] # Optional15)
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5},6{7"name": "pegasus1.2",8"options": ["visual", "audio"]9}10]11index = client.index.create(12name="<YOUR_INDEX_NAME>",13models=models,14addons=["thumbnail"] # Optional15)
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation_option
```

```plaintext
metadata
```

```plaintext
modules
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="<YOUR_QUERY>",4options=["visual", "audio"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="<YOUR_QUERY>",4options=["visual", "audio"]5)
```

```plaintext
engine*
```

```plaintext
model*
```

```plaintext
1res = client.embed.create(2model_name="Marengo-retrieval-2.7",3text="<YOUR_TEXT>",4)
```

```plaintext
1res = client.embed.create(2model_name="Marengo-retrieval-2.7",3text="<YOUR_TEXT>",4)
```

```plaintext
1res = client.generate.text(2video_id="<YOUR_VIDEO_ID>",3prompt="Classify this video using up to five labels from YouTube standard content categories. Provide the results in the JSON format."4)
```

```plaintext
1res = client.generate.text(2video_id="<YOUR_VIDEO_ID>",3prompt="Classify this video using up to five labels from YouTube standard content categories. Provide the results in the JSON format."4)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Nike",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Nike",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_media_type="image",4query_media_url="https://logodownload.org/wp-content/uploads/2013/12/apple-logo-16.png,5options=["visual"]6)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_media_type="image",4query_media_url="https://logodownload.org/wp-content/uploads/2013/12/apple-logo-16.png,5options=["visual"]6)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Innovation",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Innovation",4options=["visual"]5)
```


---

### Partner integrations {#partner-integrations}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations#explore-integration-opportunities-with-twelvelabs*

##### Adobe Premiere Pro Plugin


---

### Adobe Premiere Pro Plugin {#adobe-premiere-pro-plugin}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/adobe-premiere-pro-plugin*

### Install the plugin

Follow the steps below to add the plugin to Premiere Pro and access it from the application’s menu.

### Connect your TwelveLabs account

Connect the plugin to your TwelveLabs account:

### Assign an index to your project

Assigning an index to a Premiere Pro project determines where videos are uploaded using the plugin. However, you can search and generate chapters or highlights across other indexes.

Ingesting videos will upload your proxy files to the TwelveLabs Video Understanding Platform for processing. After processing, you can search the videos or create chapters and highlights.

Follow the steps in the sections below to search through your video content and generate chapters or highlights.

### Search for specific moments

Searching enables you to locate specific video segments by describing content in natural language. Note that you can only search videos uploaded using the plugin. Videos not uploaded via the plugin will show a “Clips not in project” banner and will be greyed out.

### Generate chapters or highlights

Generating chapters or highlights divides videos into meaningful segments, allowing you to quickly locate and work with specific sections without manually reviewing entire videos. Note that you can only generate chapters and highlights for videos uploaded using the plugin. Videos not uploaded through the plugin will display a “Clip not in project” banner and will be greyed out.

##### Voxel51 - Semantic video search plugin

#### Code Examples

```plaintext
.zxp
```


---

### ApertureDB - Semantic video search engine {#aperturedb---semantic-video-search-engine}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/aperture-db-semantic-video-search-engine*

### Video embeddings

The code below creates a video embedding task that handles the processing of a video. It periodically checks the status of the task and retrieves the embeddings upon completion:

For details on creating text embeddings, see the Create video embeddings page.

### Text embeddings

The code below creates a text embedding for the query provided in the text parameter:

For details on creating text embeddings, see the Create text embeddings page.

After reading this page, you have the following options:

- Customize and use the example: Use the TwelveLabs-EmbedAPI-ApertureDB notebook to understand how the integration works. You can make changes and add functionalities to suit your specific use case. Below are a few examples: Explore data modeling: Experiment with different video segmentation strategies to optimize embedding generation. Implement advanced search: Try multimodal queries combining text, image, and audio inputs. Scale your system: Test performance with larger video datasets and optimize for high-volume queries.
- Explore data modeling: Experiment with different video segmentation strategies to optimize embedding generation.
- Implement advanced search: Try multimodal queries combining text, image, and audio inputs.
- Scale your system: Test performance with larger video datasets and optimize for high-volume queries.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Pinecone - Multimodal RAG

#### Code Examples

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.embed import EmbeddingsTask34# Initialize the TwelveLabs client5twelvelabs_client = TwelveLabs(api_key=TL_API_KEY)67def generate_embedding(video_url):8# Create an embedding task9task = twelvelabs_client.embed.task.create(10engine_name="Marengo-retrieval-2.7",11video_url=video_url12)13print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")1415# Define a callback function to monitor task progress16def on_task_update(task: EmbeddingsTask):17print(f"  Status={task.status}")1819# Wait for the task to complete20status = task.wait_for_done(21sleep_interval=2,22callback=on_task_update23)24print(f"Embedding done: {status}")2526# Retrieve the task result27task_result = twelvelabs_client.embed.task.retrieve(task.id)2829# Extract and return the embeddings30embeddings = []31for v in task_result.video_embeddings:32embeddings.append({33'embedding': v.embedding.float,34'start_offset_sec': v.start_offset_sec,35'end_offset_sec': v.end_offset_sec,36'embedding_scope': v.embedding_scope37})3839return embeddings, task_result4041# Example usage42video_url = "https://storage.googleapis.com/ad-demos-datasets/videos/Ecommerce%20v2.5.mp4"4344# Generate embeddings for the video45embeddings, task_result = generate_embedding(video_url)4647print(f"Generated {len(embeddings)} embeddings for the video")48for i, emb in enumerate(embeddings):49print(f"Embedding {i+1}:")50print(f"  Scope: {emb['embedding_scope']}")51print(f"  Time range: {emb['start_offset_sec']} - {emb['end_offset_sec']} seconds")52print(f"  Embedding vector (first 5 values): {emb['embedding'][:5]}")53print()
```

```plaintext
1from twelvelabs import TwelveLabs2from twelvelabs.models.embed import EmbeddingsTask34# Initialize the TwelveLabs client5twelvelabs_client = TwelveLabs(api_key=TL_API_KEY)67def generate_embedding(video_url):8# Create an embedding task9task = twelvelabs_client.embed.task.create(10engine_name="Marengo-retrieval-2.7",11video_url=video_url12)13print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")1415# Define a callback function to monitor task progress16def on_task_update(task: EmbeddingsTask):17print(f"  Status={task.status}")1819# Wait for the task to complete20status = task.wait_for_done(21sleep_interval=2,22callback=on_task_update23)24print(f"Embedding done: {status}")2526# Retrieve the task result27task_result = twelvelabs_client.embed.task.retrieve(task.id)2829# Extract and return the embeddings30embeddings = []31for v in task_result.video_embeddings:32embeddings.append({33'embedding': v.embedding.float,34'start_offset_sec': v.start_offset_sec,35'end_offset_sec': v.end_offset_sec,36'embedding_scope': v.embedding_scope37})3839return embeddings, task_result4041# Example usage42video_url = "https://storage.googleapis.com/ad-demos-datasets/videos/Ecommerce%20v2.5.mp4"4344# Generate embeddings for the video45embeddings, task_result = generate_embedding(video_url)4647print(f"Generated {len(embeddings)} embeddings for the video")48for i, emb in enumerate(embeddings):49print(f"Embedding {i+1}:")50print(f"  Scope: {emb['embedding_scope']}")51print(f"  Time range: {emb['start_offset_sec']} - {emb['end_offset_sec']} seconds")52print(f"  Embedding vector (first 5 values): {emb['embedding'][:5]}")53print()
```

```plaintext
text
```

```plaintext
1# Generate a text embedding for our search query2text_embedding = twelvelabs_client.embed.create(3engine_name="Marengo-retrieval-2.7",4text="Show me the part which has lot of outfits being displayed",5text_truncate="none"6)78print("Created a text embedding")9print(f" Engine: {text_embedding.engine_name}")10print(f" Embedding: {text_embedding.text_embedding.float[:5]}...")  # Display first 5 values
```

```plaintext
1# Generate a text embedding for our search query2text_embedding = twelvelabs_client.embed.create(3engine_name="Marengo-retrieval-2.7",4text="Show me the part which has lot of outfits being displayed",5text_truncate="none"6)78print("Created a text embedding")9print(f" Engine: {text_embedding.engine_name}")10print(f" Embedding: {text_embedding.text_embedding.float[:5]}...")  # Display first 5 values
```


---

### Chroma - Multimodal RAG: Chat with Videos {#chroma---multimodal-rag-chat-with-videos}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/chroma-multimodal-rag-chat-with-videos*

##### Snowflake - Multimodal Video Understanding


---

### Databricks - Advanced video understanding {#databricks---advanced-video-understanding}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/databricks-advanced-video-understanding*

### Video embeddings

The get_video_embeddings function creates a Pandas UDF to generate multimodal embeddings using TwelveLabs Embed API:

For details on creating video embeddings, see the Create video embeddings page.

### Text embeddings

The get_text_embedding function generates text embeddings:

For details on creating video embeddings, see the Create text embeddings page.

### Similarity search

The similarity_search function generates an embedding for a text query, and uses the Mosaic AI Vector Search index to find similar videos:

### Video recommendation

The get_video_recommendations takes a video ID and the number of recommendations to return as parameters and performs a similarity search to find the most similar videos.

After reading this page, you have the following options:

- Customize and use the example: After implementing the basic integration, consider these improvements: Update and synchronize the index: Implement efficient incremental updates and scheduled synchronization jobs using Delta Lake features. Optimize performance and scaling: Leverage distributed processing, intelligent caching, and index partitioning for larger video libraries Monitoring and analytics: Track key performance metrics, implement feedback loops, and correlate capabilities with business metrics
- Update and synchronize the index: Implement efficient incremental updates and scheduled synchronization jobs using Delta Lake features.
- Optimize performance and scaling: Leverage distributed processing, intelligent caching, and index partitioning for larger video libraries
- Monitoring and analytics: Track key performance metrics, implement feedback loops, and correlate capabilities with business metrics
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Qdrant - Building a semantic video search workflow

#### Code Examples

```plaintext
get_video_embeddings
```

```plaintext
1from pyspark.sql.functions import pandas_udf2from pyspark.sql.types import ArrayType, FloatType3from twelvelabs.models.embed import EmbeddingsTask4import pandas as pd56@pandas_udf(ArrayType(FloatType()))7def get_video_embeddings(urls: pd.Series) -> pd.Series:8def generate_embedding(video_url):9twelvelabs_client = TwelveLabs(api_key=TWELVE_LABS_API_KEY)10task = twelvelabs_client.embed.task.create(11engine_name="Marengo-retrieval-2.7",12video_url=video_url13)14task.wait_for_done()15task_result = twelvelabs_client.embed.task.retrieve(task.id)16embeddings = []17for v in task_result.video_embeddings:18embeddings.append({19'embedding': v.embedding.float,20'start_offset_sec': v.start_offset_sec,21'end_offset_sec': v.end_offset_sec,22'embedding_scope': v.embedding_scope23})24return embeddings2526def process_url(url):27embeddings = generate_embedding(url)28return embeddings[0]['embedding'] if embeddings else None2930return urls.apply(process_url)
```

```plaintext
1from pyspark.sql.functions import pandas_udf2from pyspark.sql.types import ArrayType, FloatType3from twelvelabs.models.embed import EmbeddingsTask4import pandas as pd56@pandas_udf(ArrayType(FloatType()))7def get_video_embeddings(urls: pd.Series) -> pd.Series:8def generate_embedding(video_url):9twelvelabs_client = TwelveLabs(api_key=TWELVE_LABS_API_KEY)10task = twelvelabs_client.embed.task.create(11engine_name="Marengo-retrieval-2.7",12video_url=video_url13)14task.wait_for_done()15task_result = twelvelabs_client.embed.task.retrieve(task.id)16embeddings = []17for v in task_result.video_embeddings:18embeddings.append({19'embedding': v.embedding.float,20'start_offset_sec': v.start_offset_sec,21'end_offset_sec': v.end_offset_sec,22'embedding_scope': v.embedding_scope23})24return embeddings2526def process_url(url):27embeddings = generate_embedding(url)28return embeddings[0]['embedding'] if embeddings else None2930return urls.apply(process_url)
```

```plaintext
get_text_embedding
```

```plaintext
1def get_text_embedding(text_query):2# TwelveLabs Embed API supports text-to-embedding3text_embedding = twelvelabs_client.embed.create(4engine_name="Marengo-retrieval-2.7",5text=text_query,6text_truncate="start"7)89return text_embedding.text_embedding.float
```

```plaintext
1def get_text_embedding(text_query):2# TwelveLabs Embed API supports text-to-embedding3text_embedding = twelvelabs_client.embed.create(4engine_name="Marengo-retrieval-2.7",5text=text_query,6text_truncate="start"7)89return text_embedding.text_embedding.float
```

```plaintext
similarity_search
```

```plaintext
1def similarity_search(query_text, num_results=5):2# Initialize the Vector Search client and get the query embedding3mosaic_client = VectorSearchClient()4query_embedding = get_text_embedding(query_text)56print(f"Query embedding generated: {len(query_embedding)} dimensions")78# Perform the similarity search9results = index.similarity_search(10query_vector=query_embedding,11num_results=num_results,12columns=["id", "url", "title"]13)14return results
```

```plaintext
1def similarity_search(query_text, num_results=5):2# Initialize the Vector Search client and get the query embedding3mosaic_client = VectorSearchClient()4query_embedding = get_text_embedding(query_text)56print(f"Query embedding generated: {len(query_embedding)} dimensions")78# Perform the similarity search9results = index.similarity_search(10query_vector=query_embedding,11num_results=num_results,12columns=["id", "url", "title"]13)14return results
```

```plaintext
get_video_recommendations
```

```plaintext
1def get_video_recommendations(video_id, num_recommendations=5):2# Initialize the Vector Search client3mosaic_client = VectorSearchClient()45# First, retrieve the embedding for the given video_id6source_df = spark.table("videos_source_embeddings")7video_embedding = source_df.filter(f"id = {video_id}").select("embedding").first()89if not video_embedding:10print(f"No video found with id: {video_id}")11return []1213# Perform similarity search using the video's embedding14try:15results = index.similarity_search(16query_vector=video_embedding["embedding"],17num_results=num_recommendations + 1,  # +1 to account for the input video18columns=["id", "url", "title"]19)2021# Parse the results22recommendations = parse_search_results(results)2324# Remove the input video from recommendations if present25recommendations = [r for r in recommendations if r.get('id') != video_id]2627return recommendations[:num_recommendations]28except Exception as e:29print(f"Error during recommendation: {e}")30return []3132# Helper function to display recommendations33def display_recommendations(recommendations):34if recommendations:35print(f"Top {len(recommendations)} recommended videos:")36for i, video in enumerate(recommendations, 1):37print(f"{i}. Title: {video.get('title', 'N/A')}")38print(f"   URL: {video.get('url', 'N/A')}")39print(f"   Similarity Score: {video.get('score', 'N/A')}")40print()41else:42print("No recommendations found.")4344# Example usage45video_id = 1  # Assuming this is a valid video ID in your dataset46recommendations = get_video_recommendations(video_id)47display_recommendations(recommendations)
```

```plaintext
1def get_video_recommendations(video_id, num_recommendations=5):2# Initialize the Vector Search client3mosaic_client = VectorSearchClient()45# First, retrieve the embedding for the given video_id6source_df = spark.table("videos_source_embeddings")7video_embedding = source_df.filter(f"id = {video_id}").select("embedding").first()89if not video_embedding:10print(f"No video found with id: {video_id}")11return []1213# Perform similarity search using the video's embedding14try:15results = index.similarity_search(16query_vector=video_embedding["embedding"],17num_results=num_recommendations + 1,  # +1 to account for the input video18columns=["id", "url", "title"]19)2021# Parse the results22recommendations = parse_search_results(results)2324# Remove the input video from recommendations if present25recommendations = [r for r in recommendations if r.get('id') != video_id]2627return recommendations[:num_recommendations]28except Exception as e:29print(f"Error during recommendation: {e}")30return []3132# Helper function to display recommendations33def display_recommendations(recommendations):34if recommendations:35print(f"Top {len(recommendations)} recommended videos:")36for i, video in enumerate(recommendations, 1):37print(f"{i}. Title: {video.get('title', 'N/A')}")38print(f"   URL: {video.get('url', 'N/A')}")39print(f"   Similarity Score: {video.get('score', 'N/A')}")40print()41else:42print("No recommendations found.")4344# Example usage45video_id = 1  # Assuming this is a valid video ID in your dataset46recommendations = get_video_recommendations(video_id)47display_recommendations(recommendations)
```


---

### Milvus - Advanced video search {#milvus---advanced-video-search}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/milvus-advanced-video-search*

##### LanceDB - Building advanced video understanding applications

#### Code Examples

```plaintext
generate_embedding
```

```plaintext
1def generate_embedding(video_url):2"""3Generate embeddings for a given video URL using the TwelveLabs API.45This function creates an embedding task for the specified video URL using6the Marengo-retrieval-2.7 engine. It monitors the task progress and waits7for completion. Once done, it retrieves the task result and extracts the8embeddings along with their associated metadata.910Args:11video_url (str): The URL of the video to generate embeddings for.1213Returns:14tuple: A tuple containing two elements:151. list: A list of dictionaries, where each dictionary contains:16- 'embedding': The embedding vector as a list of floats.17- 'start_offset_sec': The start time of the segment in seconds.18- 'end_offset_sec': The end time of the segment in seconds.19- 'embedding_scope': The scope of the embedding (e.g., 'shot', 'scene').202. EmbeddingsTaskResult: The complete task result object from TwelveLabs API.2122Raises:23Any exceptions raised by the TwelveLabs API during task creation,24execution, or retrieval.25"""2627# Create an embedding task28task = twelvelabs_client.embed.task.create(29engine_name="Marengo-retrieval-2.7",30video_url=video_url31)32print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")3334# Define a callback function to monitor task progress35def on_task_update(task: EmbeddingsTask):36print(f"  Status={task.status}")3738# Wait for the task to complete39status = task.wait_for_done(40sleep_interval=2,41callback=on_task_update42)43print(f"Embedding done: {status}")4445# Retrieve the task result46task_result = twelvelabs_client.embed.task.retrieve(task.id)4748# Extract and return the embeddings49embeddings = []50for v in task_result.video_embeddings:51embeddings.append({52'embedding': v.embedding.float,53'start_offset_sec': v.start_offset_sec,54'end_offset_sec': v.end_offset_sec,55'embedding_scope': v.embedding_scope56})5758return embeddings, task_result
```

```plaintext
1def generate_embedding(video_url):2"""3Generate embeddings for a given video URL using the TwelveLabs API.45This function creates an embedding task for the specified video URL using6the Marengo-retrieval-2.7 engine. It monitors the task progress and waits7for completion. Once done, it retrieves the task result and extracts the8embeddings along with their associated metadata.910Args:11video_url (str): The URL of the video to generate embeddings for.1213Returns:14tuple: A tuple containing two elements:151. list: A list of dictionaries, where each dictionary contains:16- 'embedding': The embedding vector as a list of floats.17- 'start_offset_sec': The start time of the segment in seconds.18- 'end_offset_sec': The end time of the segment in seconds.19- 'embedding_scope': The scope of the embedding (e.g., 'shot', 'scene').202. EmbeddingsTaskResult: The complete task result object from TwelveLabs API.2122Raises:23Any exceptions raised by the TwelveLabs API during task creation,24execution, or retrieval.25"""2627# Create an embedding task28task = twelvelabs_client.embed.task.create(29engine_name="Marengo-retrieval-2.7",30video_url=video_url31)32print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")3334# Define a callback function to monitor task progress35def on_task_update(task: EmbeddingsTask):36print(f"  Status={task.status}")3738# Wait for the task to complete39status = task.wait_for_done(40sleep_interval=2,41callback=on_task_update42)43print(f"Embedding done: {status}")4445# Retrieve the task result46task_result = twelvelabs_client.embed.task.retrieve(task.id)4748# Extract and return the embeddings49embeddings = []50for v in task_result.video_embeddings:51embeddings.append({52'embedding': v.embedding.float,53'start_offset_sec': v.start_offset_sec,54'end_offset_sec': v.end_offset_sec,55'embedding_scope': v.embedding_scope56})5758return embeddings, task_result
```


---

### MindsDB - The TwelveLabs handler {#mindsdb---the-twelvelabs-handler}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/minds-db-the-twelve-labs-handler*

### Initialize a client

The constructor sets up a new TwelveLabsAPIClient object that establishes a connection to the TwelveLabs Video Understanding Platform:

### Create indexes

To create indexes, the create_index method invokes the POST method of the /indexes endpoint:

### Upload videos

To upload videos to the TwelveLabs Video Understanding Platform and index them, the handler invokes the POST method of the /tasks endpoint:

Once the video has been uploaded to the platform, the handler monitors the indexing process using the GET method of the /tasks/{task_id} endpoint:

### Perform downstream tasks

The handler supports the following downstream tasks - search and summarize videos. See the sections below for details.

#### Search videos

To perform search requests, the handler invokes the POST method of the /search endpoint:

#### Summarize videos

To summarize videos, the handler invokes the POST method of the summarize endpoint:

After reading this page, you have several options:

- Use the handler: Inspect the TwelveLabs Handler page on GitHub to better understand its features and start using it in your applications.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Backblaze B2 - Media management application

#### Code Examples

```plaintext
$pip install mindsdb[twelve_labs]
```

```plaintext
$pip install mindsdb[twelve_labs]
```

```plaintext
CREATE ML_ENGINE
```

```plaintext
<>
```

```plaintext
1CREATE ML_ENGINE <YOUR_ENGINE_NAME>2from twelve_labs3USING4twelve_labs_api_key = '<YOUR_API_KEY>'
```

```plaintext
1CREATE ML_ENGINE <YOUR_ENGINE_NAME>2from twelve_labs3USING4twelve_labs_api_key = '<YOUR_API_KEY>'
```

```plaintext
twelve_labs_engine
```

```plaintext
1CREATE ML_ENGINE twelve_labs_engine2from twelve_labs3USING4twelve_labs_api_key = 'tlk_111'
```

```plaintext
1CREATE ML_ENGINE twelve_labs_engine2from twelve_labs3USING4twelve_labs_api_key = 'tlk_111'
```

```plaintext
CREATE_MODEL
```

```plaintext
PREDICT
```

```plaintext
USING
```

```plaintext
search
```

```plaintext
summarization
```

```plaintext
search
```

```plaintext
1CREATE MODEL mindsdb.twelve_labs_search2PREDICT search_results3USING4engine = 'twelve_labs_engine',5task = 'search',6engine_id = 'marengo2.7',7index_name = 'index_1',8index_options = ['visual', 'conversation', 'text_in_video', 'logo'],9video_urls = ['https://.../video_1.mp4', 'https://.../video_2.mp4'],10search_options = ['visual', 'conversation', 'text_in_video', 'logo'],11search_query_column = 'query';
```

```plaintext
1CREATE MODEL mindsdb.twelve_labs_search2PREDICT search_results3USING4engine = 'twelve_labs_engine',5task = 'search',6engine_id = 'marengo2.7',7index_name = 'index_1',8index_options = ['visual', 'conversation', 'text_in_video', 'logo'],9video_urls = ['https://.../video_1.mp4', 'https://.../video_2.mp4'],10search_options = ['visual', 'conversation', 'text_in_video', 'logo'],11search_query_column = 'query';
```

```plaintext
summarization
```

```plaintext
1CREATE MODEL mindsdb.twelve_labs_summarization2PREDICT summarization_results3USING4engine = 'twelve_labs_engine',5task = 'summarization',6engine_id = 'pegasus1',7index_name = 'index_1',8index_options = ['visual', 'conversation'],9video_urls = ['https://.../video_1.mp4', 'https://.../video_2.mp4'],10summarization_type = 'summary';
```

```plaintext
1CREATE MODEL mindsdb.twelve_labs_summarization2PREDICT summarization_results3USING4engine = 'twelve_labs_engine',5task = 'summarization',6engine_id = 'pegasus1',7index_name = 'index_1',8index_options = ['visual', 'conversation'],9video_urls = ['https://.../video_1.mp4', 'https://.../video_2.mp4'],10summarization_type = 'summary';
```

```plaintext
DESCRIBE
```

```plaintext
<>
```

```plaintext
1DESCRIBE mindsdb.<YOUR_MODEL_NAME>;
```

```plaintext
1DESCRIBE mindsdb.<YOUR_MODEL_NAME>;
```

```plaintext
twelve_labs_summarization
```

```plaintext
DESCRIBE mindsdb.twelve_labs_summarization;
```

```plaintext
DESCRIBE mindsdb.twelve_labs_summarization;
```

```plaintext
complete
```

```plaintext
STATUS
```

```plaintext
ERROR
```

```plaintext
DESCRIBE
```

```plaintext
indexed_videos
```

```plaintext
<>
```

```plaintext
DESCRIBE mindsdb.<YOUR_MODEL_NAME>.indexed_videos;
```

```plaintext
DESCRIBE mindsdb.<YOUR_MODEL_NAME>.indexed_videos;
```

```plaintext
twelve_labs_summarization
```

```plaintext
DESCRIBE mindsdb.twelve_labs_summarization.indexed_videos;
```

```plaintext
DESCRIBE mindsdb.twelve_labs_summarization.indexed_videos;
```

```plaintext
SELECT
```

```plaintext
WHERE
```

```plaintext
search
```

```plaintext
summarization
```

```plaintext
<>
```

```plaintext
<>
```

```plaintext
1SELECT *2FROM mindsdb.<YOUR_MODEL_NAME>3WHERE query = '<YOUR_QUERY>';
```

```plaintext
1SELECT *2FROM mindsdb.<YOUR_MODEL_NAME>3WHERE query = '<YOUR_QUERY>';
```

```plaintext
twelve_labs_search
```

```plaintext
1SELECT *2FROM mindsdb.twelve_labs_search3WHERE query = 'Soccer player scoring a goal';
```

```plaintext
1SELECT *2FROM mindsdb.twelve_labs_search3WHERE query = 'Soccer player scoring a goal';
```

```plaintext
<>
```

```plaintext
1SELECT *2FROM mindsdb.<YOUR_MODEL_NAME>3WHERE video_id = '<YOUR_VIDEO_ID>';
```

```plaintext
1SELECT *2FROM mindsdb.<YOUR_MODEL_NAME>3WHERE video_id = '<YOUR_VIDEO_ID>';
```

```plaintext
twelve_labs_summarization
```

```plaintext
1SELECT *2FROM mindsdb.twelve_labs_summarization3WHERE video_id = '660bfa6766995fbd9fd662ee';
```

```plaintext
1SELECT *2FROM mindsdb.twelve_labs_summarization3WHERE video_id = '660bfa6766995fbd9fd662ee';
```

```plaintext
TwelveLabsAPIClient
```

```plaintext
1def __init__(self, api_key: str, base_url: str = None):2"""3The initializer for the TwelveLabsAPIClient.45Parameters6----------7api_key : str8The TwelveLabs API key.9base_url : str, Optional10The base URL for the TwelveLabs API. Defaults to the base URL in the TwelveLabs handler settings.11"""1213self.api_key = api_key14self.headers = {15'Content-Type': 'application/json',16'x-api-key': self.api_key17}18self.base_url = base_url if base_url else twelve_labs_handler_config.BASE_URL
```

```plaintext
1def __init__(self, api_key: str, base_url: str = None):2"""3The initializer for the TwelveLabsAPIClient.45Parameters6----------7api_key : str8The TwelveLabs API key.9base_url : str, Optional10The base URL for the TwelveLabs API. Defaults to the base URL in the TwelveLabs handler settings.11"""1213self.api_key = api_key14self.headers = {15'Content-Type': 'application/json',16'x-api-key': self.api_key17}18self.base_url = base_url if base_url else twelve_labs_handler_config.BASE_URL
```

```plaintext
create_index
```

```plaintext
POST
```

```plaintext
/indexes
```

```plaintext
1def create_index(self, index_name: str, index_options: List[str], engine_id: Optional[str] = None, addons: Optional[List[str]] = None) -> str:2"""3Create an index.45Parameters6----------7index_name : str8Name of the index to be created.910index_options : List[str]11List of that specifies how the platform will process the videos uploaded to this index.1213engine_id : str, Optional14ID of the engine. If not provided, the default engine is used.1516addons : List[str], Optional17List of addons that should be enabled for the index.1819Returns20-------21str22ID of the created index.23"""2425# TODO: change index_options to engine_options?26# TODO: support multiple engines per index?27body = {28"index_name": index_name,29"engines": [{30"engine_name": engine_id if engine_id else twelve_labs_handler_config.DEFAULT_ENGINE_ID,31"engine_options": index_options32}],33"addons": addons,34}3536result = self._submit_request(37method="POST",38endpoint="/indexes",39data=body,40)4142logger.info(f"Index {index_name} successfully created.")43return result['_id']
```

```plaintext
1def create_index(self, index_name: str, index_options: List[str], engine_id: Optional[str] = None, addons: Optional[List[str]] = None) -> str:2"""3Create an index.45Parameters6----------7index_name : str8Name of the index to be created.910index_options : List[str]11List of that specifies how the platform will process the videos uploaded to this index.1213engine_id : str, Optional14ID of the engine. If not provided, the default engine is used.1516addons : List[str], Optional17List of addons that should be enabled for the index.1819Returns20-------21str22ID of the created index.23"""2425# TODO: change index_options to engine_options?26# TODO: support multiple engines per index?27body = {28"index_name": index_name,29"engines": [{30"engine_name": engine_id if engine_id else twelve_labs_handler_config.DEFAULT_ENGINE_ID,31"engine_options": index_options32}],33"addons": addons,34}3536result = self._submit_request(37method="POST",38endpoint="/indexes",39data=body,40)4142logger.info(f"Index {index_name} successfully created.")43return result['_id']
```

```plaintext
/tasks
```

```plaintext
1def create_video_indexing_tasks(self, index_id: str, video_urls: List[str] = None, video_files: List[str] = None) -> List[str]:2"""3Create video indexing tasks.45Parameters6----------7index_id : str8ID of the index.910video_urls : List[str], Optional11List of video urls to be indexed. Either video_urls or video_files should be provided. This validation is handled by TwelveLabsHandlerModel.1213video_files : List[str], Optional14List of video files to be indexed. Either video_urls or video_files should be provided. This validation is handled by TwelveLabsHandlerModel.1516Returns17-------18List[str]19List of task IDs created.20"""2122task_ids = []2324if video_urls:25logger.info("video_urls has been set, therefore, it will be given precedence.")26logger.info("Creating video indexing tasks for video urls.")2728for video_url in video_urls:29task_ids.append(30self._create_video_indexing_task(31index_id=index_id,32video_url=video_url33)34)3536elif video_files:37logger.info("video_urls has not been set, therefore, video_files will be used.")38logger.info("Creating video indexing tasks for video files.")39for video_file in video_files:40task_ids.append(41self._create_video_indexing_task(42index_id=index_id,43video_file=video_file44)45)4647return task_ids4849def _create_video_indexing_task(self, index_id: str, video_url: str = None, video_file: str = None) -> str:50"""51Create a video indexing task.5253Parameters54----------55index_id : str56ID of the index.5758video_url : str, Optional59URL of the video to be indexed. Either video_url or video_file should be provided. This validation is handled by TwelveLabsHandlerModel.6061video_file : str, Optional62Path to the video file to be indexed. Either video_url or video_file should be provided. This validation is handled by TwelveLabsHandlerModel.6364Returns65-------66str67ID of the created task.68"""6970body = {71"index_id": index_id,72}7374file_to_close = None75if video_url:76body['video_url'] = video_url7778elif video_file:79import mimetypes80# WE need the file open for the duration of the request. Maybe simplify it with context manager later, but needs _create_video_indexing_task re-written81file_to_close = open(video_file, 'rb')82mime_type, _ = mimetypes.guess_type(video_file)83body['video_file'] = (file_to_close.name, file_to_close, mime_type)8485result = self._submit_multi_part_request(86method="POST",87endpoint="/tasks",88data=body,89)9091if file_to_close:92file_to_close.close()9394task_id = result['_id']95logger.info(f"Created video indexing task {task_id} for {video_url if video_url else video_file} successfully.")9697# update the video title98video_reference = video_url if video_url else video_file99task = self._get_video_indexing_task(task_id=task_id)100self._update_video_metadata(101index_id=index_id,102video_id=task['video_id'],103metadata={104"video_reference": video_reference105}106)107108return task_id
```

```plaintext
1def create_video_indexing_tasks(self, index_id: str, video_urls: List[str] = None, video_files: List[str] = None) -> List[str]:2"""3Create video indexing tasks.45Parameters6----------7index_id : str8ID of the index.910video_urls : List[str], Optional11List of video urls to be indexed. Either video_urls or video_files should be provided. This validation is handled by TwelveLabsHandlerModel.1213video_files : List[str], Optional14List of video files to be indexed. Either video_urls or video_files should be provided. This validation is handled by TwelveLabsHandlerModel.1516Returns17-------18List[str]19List of task IDs created.20"""2122task_ids = []2324if video_urls:25logger.info("video_urls has been set, therefore, it will be given precedence.")26logger.info("Creating video indexing tasks for video urls.")2728for video_url in video_urls:29task_ids.append(30self._create_video_indexing_task(31index_id=index_id,32video_url=video_url33)34)3536elif video_files:37logger.info("video_urls has not been set, therefore, video_files will be used.")38logger.info("Creating video indexing tasks for video files.")39for video_file in video_files:40task_ids.append(41self._create_video_indexing_task(42index_id=index_id,43video_file=video_file44)45)4647return task_ids4849def _create_video_indexing_task(self, index_id: str, video_url: str = None, video_file: str = None) -> str:50"""51Create a video indexing task.5253Parameters54----------55index_id : str56ID of the index.5758video_url : str, Optional59URL of the video to be indexed. Either video_url or video_file should be provided. This validation is handled by TwelveLabsHandlerModel.6061video_file : str, Optional62Path to the video file to be indexed. Either video_url or video_file should be provided. This validation is handled by TwelveLabsHandlerModel.6364Returns65-------66str67ID of the created task.68"""6970body = {71"index_id": index_id,72}7374file_to_close = None75if video_url:76body['video_url'] = video_url7778elif video_file:79import mimetypes80# WE need the file open for the duration of the request. Maybe simplify it with context manager later, but needs _create_video_indexing_task re-written81file_to_close = open(video_file, 'rb')82mime_type, _ = mimetypes.guess_type(video_file)83body['video_file'] = (file_to_close.name, file_to_close, mime_type)8485result = self._submit_multi_part_request(86method="POST",87endpoint="/tasks",88data=body,89)9091if file_to_close:92file_to_close.close()9394task_id = result['_id']95logger.info(f"Created video indexing task {task_id} for {video_url if video_url else video_file} successfully.")9697# update the video title98video_reference = video_url if video_url else video_file99task = self._get_video_indexing_task(task_id=task_id)100self._update_video_metadata(101index_id=index_id,102video_id=task['video_id'],103metadata={104"video_reference": video_reference105}106)107108return task_id
```

```plaintext
/tasks/{task_id}
```

```plaintext
1def poll_for_video_indexing_tasks(self, task_ids: List[str]) -> None:2"""3Poll for video indexing tasks to complete.45Parameters6----------7task_ids : List[str]8List of task IDs to be polled.910Returns11-------12None13"""1415for task_id in task_ids:16logger.info(f"Polling status of video indexing task {task_id}.")17is_task_running = True1819while is_task_running:20task = self._get_video_indexing_task(task_id=task_id)21status = task['status']22logger.info(f"Task {task_id} is in the {status} state.")2324wait_durtion = task['process']['remain_seconds'] if 'process' in task else twelve_labs_handler_config.DEFAULT_WAIT_DURATION2526if status in ('pending', 'indexing', 'validating'):27logger.info(f"Task {task_id} will be polled again in {wait_durtion} seconds.")28time.sleep(wait_durtion)2930elif status == 'ready':31logger.info(f"Task {task_id} completed successfully.")32is_task_running = False3334else:35logger.error(f"Task {task_id} failed with status {task['status']}.")36# TODO: update Exception to be more specific37raise Exception(f"Task {task_id} failed with status {task['status']}.")3839logger.info("All videos indexed successffully.")
```

```plaintext
1def poll_for_video_indexing_tasks(self, task_ids: List[str]) -> None:2"""3Poll for video indexing tasks to complete.45Parameters6----------7task_ids : List[str]8List of task IDs to be polled.910Returns11-------12None13"""1415for task_id in task_ids:16logger.info(f"Polling status of video indexing task {task_id}.")17is_task_running = True1819while is_task_running:20task = self._get_video_indexing_task(task_id=task_id)21status = task['status']22logger.info(f"Task {task_id} is in the {status} state.")2324wait_durtion = task['process']['remain_seconds'] if 'process' in task else twelve_labs_handler_config.DEFAULT_WAIT_DURATION2526if status in ('pending', 'indexing', 'validating'):27logger.info(f"Task {task_id} will be polled again in {wait_durtion} seconds.")28time.sleep(wait_durtion)2930elif status == 'ready':31logger.info(f"Task {task_id} completed successfully.")32is_task_running = False3334else:35logger.error(f"Task {task_id} failed with status {task['status']}.")36# TODO: update Exception to be more specific37raise Exception(f"Task {task_id} failed with status {task['status']}.")3839logger.info("All videos indexed successffully.")
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
1def search_index(self, index_id: str, query: str, search_options: List[str]) -> Dict:2"""3Search an index.45Parameters6----------7index_id : str8ID of the index.910query : str11Query to be searched.1213search_options : List[str]14List of search options to be used.1516Returns17-------18Dict19Search results.20"""2122body = {23"index_id": index_id,24"query": query,25"search_options": search_options26}2728data = []29result = self._submit_request(30method="POST",31endpoint="/search",32data=body,33)34data.extend(result['data'])3536while 'next_page_token' in result['page_info']:37result = self._submit_request(38method="GET",39endpoint=f"/search/{result['page_info']['next_page_token']}"40)41data.extend(result['data'])4243logger.info(f"Search for index {index_id} completed successfully.")44return data
```

```plaintext
1def search_index(self, index_id: str, query: str, search_options: List[str]) -> Dict:2"""3Search an index.45Parameters6----------7index_id : str8ID of the index.910query : str11Query to be searched.1213search_options : List[str]14List of search options to be used.1516Returns17-------18Dict19Search results.20"""2122body = {23"index_id": index_id,24"query": query,25"search_options": search_options26}2728data = []29result = self._submit_request(30method="POST",31endpoint="/search",32data=body,33)34data.extend(result['data'])3536while 'next_page_token' in result['page_info']:37result = self._submit_request(38method="GET",39endpoint=f"/search/{result['page_info']['next_page_token']}"40)41data.extend(result['data'])4243logger.info(f"Search for index {index_id} completed successfully.")44return data
```

```plaintext
POST
```

```plaintext
summarize
```

```plaintext
1def summarize_videos(self, video_ids: List[str], summarization_type: str, prompt: str) -> Dict:2"""3Summarize videos.45Parameters6----------7video_ids : List[str]8List of video IDs.910summarization_type : str11Type of the summary to be generated. Supported types are 'summary', 'chapter' and 'highlight'.1213prompt: str14Prompt to be used for the Summarize task1516Returns17-------18Dict19Summary of the videos.20"""2122results = []23results = [self.summarize_video(video_id, summarization_type, prompt) for video_id in video_ids]2425logger.info(f"Summarized videos {video_ids} successfully.")26return results2728def summarize_video(self, video_id: str, summarization_type: str, prompt: str) -> Dict:29"""30Summarize a video.3132Parameters33----------34video_id : str35ID of the video.3637summarization_type : str38Type of the summary to be generated. Supported types are 'summary', 'chapter' and 'highlight'.3940prompt: str41Prompt to be used for the Summarize task4243Returns44-------45Dict46Summary of the video.47"""48body = {49"video_id": video_id,50"type": summarization_type,51"prompt": prompt52}5354result = self._submit_request(55method="POST",56endpoint="/summarize",57data=body,58)5960logger.info(f"Video {video_id} summarized successfully.")61return result
```

```plaintext
1def summarize_videos(self, video_ids: List[str], summarization_type: str, prompt: str) -> Dict:2"""3Summarize videos.45Parameters6----------7video_ids : List[str]8List of video IDs.910summarization_type : str11Type of the summary to be generated. Supported types are 'summary', 'chapter' and 'highlight'.1213prompt: str14Prompt to be used for the Summarize task1516Returns17-------18Dict19Summary of the videos.20"""2122results = []23results = [self.summarize_video(video_id, summarization_type, prompt) for video_id in video_ids]2425logger.info(f"Summarized videos {video_ids} successfully.")26return results2728def summarize_video(self, video_id: str, summarization_type: str, prompt: str) -> Dict:29"""30Summarize a video.3132Parameters33----------34video_id : str35ID of the video.3637summarization_type : str38Type of the summary to be generated. Supported types are 'summary', 'chapter' and 'highlight'.3940prompt: str41Prompt to be used for the Summarize task4243Returns44-------45Dict46Summary of the video.47"""48body = {49"video_id": video_id,50"type": summarization_type,51"prompt": prompt52}5354result = self._submit_request(55method="POST",56endpoint="/summarize",57data=body,58)5960logger.info(f"Video {video_id} summarized successfully.")61return result
```


---

### MongoDB - Semantic video search {#mongodb---semantic-video-search}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/mongo-db-semantic-video-search*

### Video embeddings

The code below creates a video embedding task that handles the uploading and processing of a video. It periodically checks the status of the task and retrieves the embeddings upon completion:

For more details, see the Create video embeddings page.

### Text embeddings

The code below creates a text embedding for the query provided in the text parameter:

For more details, see the Create text embeddings page.

After reading this page, you have the following options:

- Customize and use the example: Use the TwelveLabs-EmbedAPI-MongoDB-Atlas notebook to understand how the integration works. You can make changes and add more functionalities to suit your specific use case.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Milvus - Advanced video search

#### Code Examples

```plaintext
1# Create a video embedding task for the uploaded video2task = tl_client.embed.task.create(3engine_name="Marengo-retrieval-2.7",4video_url="your-video-url"5)6print(7f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}"8)910# Monitor the status of the video embedding task11def on_task_update(task: EmbeddingsTask):12print(f"  Status={task.status}")1314status = task.wait_for_done(15sleep_interval=2,16callback=on_task_update17)18print(f"Embedding done: {status}")1920# Retrieve the video embeddings21task_result = tl_client.embed.task.retrieve(task.id)
```

```plaintext
1# Create a video embedding task for the uploaded video2task = tl_client.embed.task.create(3engine_name="Marengo-retrieval-2.7",4video_url="your-video-url"5)6print(7f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}"8)910# Monitor the status of the video embedding task11def on_task_update(task: EmbeddingsTask):12print(f"  Status={task.status}")1314status = task.wait_for_done(15sleep_interval=2,16callback=on_task_update17)18print(f"Embedding done: {status}")1920# Retrieve the video embeddings21task_result = tl_client.embed.task.retrieve(task.id)
```

```plaintext
text
```

```plaintext
1# Create a text embedding task for the text2embedding = tl_client.embed.create(3engine_name="Marengo-retrieval-2.7",4text="your-text"5)67print("Created a text embedding")8print(f" Engine: {embedding.engine_name}")9print(f" Embedding: {embedding.text_embedding.float}")
```

```plaintext
1# Create a text embedding task for the text2embedding = tl_client.embed.create(3engine_name="Marengo-retrieval-2.7",4text="your-text"5)67print("Created a text embedding")8print(f" Engine: {embedding.engine_name}")9print(f" Embedding: {embedding.text_embedding.float}")
```


---

### Oracle - Unleashing Video Intelligence {#oracle---unleashing-video-intelligence}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/oracle-unleashing-video-intelligence*

##### From the community


---

### Pinecone - Multimodal RAG {#pinecone---multimodal-rag}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/pinecone-multimodal-rag*

### Video Embeddings

The generate_embedding function generates embeddings for a video file:

For details on creating video embeddings, see the Create video embeddings page.

The ingest_data function stores embeddings in Pinecone:

### Video search

The search_video_segments function creates text embeddings and performs similarity searches to find relevant video segments using the embeddings that have already been stored in Pinecone:

For details on creating text embeddings, see the Create text embeddings page.

### Natural language responses

After retrieving relevant video segments, the application uses the Analyze API to create natural language responses:

For details on analyzing videos and generating open-ended texts from their content see the Open-ended analysis page.

### Create a complete Q&A function

The application creates a complete Q&A function by combining search and response generation:

After reading this page, you have the following options:

- Customize and use the example: Use the TwelveLabs_Pinecone_Chat_with_video notebook to understand how the integration works. You can make changes and add functionalities to suit your specific use case. Below are a few examples: Training a linear adapter on top of the embeddings to better fit your data. Re-ranking videos using Pegasus when clips from different videos are returned. Adding textual summary data for each video to the Pinecone entries to create a hybrid search system, enhancing accuracy using Pinecone’s Metadata capabilities.
- Training a linear adapter on top of the embeddings to better fit your data.
- Re-ranking videos using Pegasus when clips from different videos are returned.
- Adding textual summary data for each video to the Pinecone entries to create a hybrid search system, enhancing accuracy using Pinecone’s Metadata capabilities.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Databricks - Advanced video understanding

#### Code Examples

```plaintext
generate_embedding
```

```plaintext
1def generate_embedding(video_file, engine="Marengo-retrieval-2.7"):2"""3Generate embeddings for a video file using TwelveLabs API.45Args:6video_file (str): Path to the video file7engine (str): Embedding engine name89Returns:10tuple: Embeddings and metadata11"""12# Create an embedding task13task = twelvelabs_client.embed.task.create(14engine_name=engine,15video_file=video_file16)17print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")1819# Monitor task progress20def on_task_update(task: EmbeddingsTask):21print(f"  Status={task.status}")2223status = task.wait_for_done(24sleep_interval=2,25callback=on_task_update26)27print(f"Embedding done: {status}")2829# Retrieve results30task_result = twelvelabs_client.embed.task.retrieve(task.id)3132# Extract embeddings and metadata33embeddings = task_result.float34time_ranges = task_result.time_ranges35scope = task_result.scope3637return embeddings, time_ranges, scope
```

```plaintext
1def generate_embedding(video_file, engine="Marengo-retrieval-2.7"):2"""3Generate embeddings for a video file using TwelveLabs API.45Args:6video_file (str): Path to the video file7engine (str): Embedding engine name89Returns:10tuple: Embeddings and metadata11"""12# Create an embedding task13task = twelvelabs_client.embed.task.create(14engine_name=engine,15video_file=video_file16)17print(f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}")1819# Monitor task progress20def on_task_update(task: EmbeddingsTask):21print(f"  Status={task.status}")2223status = task.wait_for_done(24sleep_interval=2,25callback=on_task_update26)27print(f"Embedding done: {status}")2829# Retrieve results30task_result = twelvelabs_client.embed.task.retrieve(task.id)3132# Extract embeddings and metadata33embeddings = task_result.float34time_ranges = task_result.time_ranges35scope = task_result.scope3637return embeddings, time_ranges, scope
```

```plaintext
ingest_data
```

```plaintext
1def ingest_data(video_file, index_name="twelve-labs"):2"""3Generate embeddings and store them in Pinecone.45Args:6video_file (str): Path to the video file7index_name (str): Name of the Pinecone index8"""9# Generate embeddings10embeddings, time_ranges, scope = generate_embedding(video_file)1112# Connect to Pinecone index13index = pc.Index(index_name)1415# Prepare vectors for upsert16vectors = []17for i, embedding in enumerate(embeddings):18vectors.append({19"id": f"{video_file}_{i}",20"values": embedding,21"metadata": {22"video_file": video_file,23"time_range": time_ranges[i],24"scope": scope25}26})2728# Upsert vectors to Pinecone29index.upsert(vectors=vectors)30print(f"Successfully ingested {len(vectors)} embeddings into Pinecone")
```

```plaintext
1def ingest_data(video_file, index_name="twelve-labs"):2"""3Generate embeddings and store them in Pinecone.45Args:6video_file (str): Path to the video file7index_name (str): Name of the Pinecone index8"""9# Generate embeddings10embeddings, time_ranges, scope = generate_embedding(video_file)1112# Connect to Pinecone index13index = pc.Index(index_name)1415# Prepare vectors for upsert16vectors = []17for i, embedding in enumerate(embeddings):18vectors.append({19"id": f"{video_file}_{i}",20"values": embedding,21"metadata": {22"video_file": video_file,23"time_range": time_ranges[i],24"scope": scope25}26})2728# Upsert vectors to Pinecone29index.upsert(vectors=vectors)30print(f"Successfully ingested {len(vectors)} embeddings into Pinecone")
```

```plaintext
search_video_segments
```

```plaintext
1def search_video_segments(question, index_name="twelve-labs", top_k=5):2"""3Search for relevant video segments based on a question.45Args:6question (str): Question text7index_name (str): Name of the Pinecone index8top_k (int): Number of results to retrieve910Returns:11list: Relevant video segments and their metadata12"""13# Generate text embedding for the question14question_embedding = twelvelabs_client.embed.create(15engine_name="Marengo-retrieval-2.7",16text=question17).text_embedding.float1819# Query Pinecone20index = pc.Index(index_name)21query_results = index.query(22vector=question_embedding,23top_k=top_k,24include_metadata=True25)2627# Process and return results28results = []29for match in query_results.matches:30results.append({31"score": match.score,32"video_file": match.metadata["video_file"],33"time_range": match.metadata["time_range"],34"scope": match.metadata["scope"]35})3637return results
```

```plaintext
1def search_video_segments(question, index_name="twelve-labs", top_k=5):2"""3Search for relevant video segments based on a question.45Args:6question (str): Question text7index_name (str): Name of the Pinecone index8top_k (int): Number of results to retrieve910Returns:11list: Relevant video segments and their metadata12"""13# Generate text embedding for the question14question_embedding = twelvelabs_client.embed.create(15engine_name="Marengo-retrieval-2.7",16text=question17).text_embedding.float1819# Query Pinecone20index = pc.Index(index_name)21query_results = index.query(22vector=question_embedding,23top_k=top_k,24include_metadata=True25)2627# Process and return results28results = []29for match in query_results.matches:30results.append({31"score": match.score,32"video_file": match.metadata["video_file"],33"time_range": match.metadata["time_range"],34"scope": match.metadata["scope"]35})3637return results
```

```plaintext
1def generate_response(question, video_segments):2"""3Generate a natural language response using Pegasus.45Args:6question (str): The user's question7video_segments (list): Relevant video segments from search89Returns:10str: Generated response based on video content11"""12# Prepare context from video segments13context = []14for segment in video_segments:15# Get the video clip based on time range16video_file = segment["video_file"]17start_time, end_time = segment["time_range"]1819# You can extract the clip or use the metadata directly20context.append({21"content": f"Video segment from {video_file}, {start_time}s to {end_time}s",22"score": segment["score"]23})2425# Generate response using TwelveLabs Analyze API26response = twelvelabs_client.generate.create(27engine_name="Pegasus-1.0",28prompt=question,29contexts=context,30max_tokens=25031)3233return response.generated_text
```

```plaintext
1def generate_response(question, video_segments):2"""3Generate a natural language response using Pegasus.45Args:6question (str): The user's question7video_segments (list): Relevant video segments from search89Returns:10str: Generated response based on video content11"""12# Prepare context from video segments13context = []14for segment in video_segments:15# Get the video clip based on time range16video_file = segment["video_file"]17start_time, end_time = segment["time_range"]1819# You can extract the clip or use the metadata directly20context.append({21"content": f"Video segment from {video_file}, {start_time}s to {end_time}s",22"score": segment["score"]23})2425# Generate response using TwelveLabs Analyze API26response = twelvelabs_client.generate.create(27engine_name="Pegasus-1.0",28prompt=question,29contexts=context,30max_tokens=25031)3233return response.generated_text
```

```plaintext
1def video_qa(question, index_name="twelve-labs"):2"""3Complete video Q&A pipeline.45Args:6question (str): User's question7index_name (str): Pinecone index name89Returns:10dict: Response with answer and supporting video segments11"""12# Find relevant video segments13video_segments = search_video_segments(question, index_name)1415# Generate response using Pegasus16answer = generate_response(question, video_segments)1718return {19"question": question,20"answer": answer,21"supporting_segments": video_segments22}
```

```plaintext
1def video_qa(question, index_name="twelve-labs"):2"""3Complete video Q&A pipeline.45Args:6question (str): User's question7index_name (str): Pinecone index name89Returns:10dict: Response with answer and supporting video segments11"""12# Find relevant video segments13video_segments = search_video_segments(question, index_name)1415# Generate response using Pegasus16answer = generate_response(question, video_segments)1718return {19"question": question,20"answer": answer,21"supporting_segments": video_segments22}
```


---

### Qdrant - Building a semantic video search workflow {#qdrant---building-a-semantic-video-search-workflow}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/qdrant-building-a-semantic-video-search-workflow*

### Video embeddings

The following code generates an embedding for a video. It creates a video embedding task that processes the video and periodically checks the task’s status to retrieve the embeddings upon completion.

For details on creating text embeddings, see the Create video embeddings page.

### Text embeddings

The code below generates a text embedding and identifies the video segments that match your text semantically.

For details on creating text embeddings, see the Create text embeddings page.

### Audio embeddings

The code below generates an audio embedding and finds the video segments that match the semantic content of your audio clip.

For details on creating text embeddings, see the Create audio embeddings page.

### Image embeddings

The code below generates an image embedding and identifies video segments that are semantically similar to the image.

For details on creating image embeddings, see the Create image embeddings page.

After reading this page, you have the following options:

- Customize and use the example: Use the TwelveLabs-EmbedAPI-Qdrant notebook to understand how the integration works. You can make changes and add functionalities to suit your specific use case.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Vespa - Multivector video retrieval

#### Code Examples

```plaintext
1# Step 1: Create an embedding task2task = twelvelabs_client.embed.task.create(3model_name="Marengo-retrieval-2.7",  # Specify the model4video_url="https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4"  # Video URL5)67# Step 2: Wait for the task to complete8task.wait_for_done(sleep_interval=3)  # Check every 3 seconds910# Step 3: Retrieve the embeddings11task_result = twelvelabs_client.embed.task.retrieve(task.id)1213# Display the embedding results14print("Embedding Vector (First 10 Dimensions):", task_result.embeddings[:10])15print("Embedding Dimensionality:", len(task_result.embeddings))
```

```plaintext
1# Step 1: Create an embedding task2task = twelvelabs_client.embed.task.create(3model_name="Marengo-retrieval-2.7",  # Specify the model4video_url="https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4"  # Video URL5)67# Step 2: Wait for the task to complete8task.wait_for_done(sleep_interval=3)  # Check every 3 seconds910# Step 3: Retrieve the embeddings11task_result = twelvelabs_client.embed.task.retrieve(task.id)1213# Display the embedding results14print("Embedding Vector (First 10 Dimensions):", task_result.embeddings[:10])15print("Embedding Dimensionality:", len(task_result.embeddings))
```

```plaintext
1# Generate text embedding2text_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4text="A white rabbit",  # Input query5).text_embedding.segments[0]67# Perform semantic search in Qdrant8text_results = qdrant_client.query_points(9collection_name=collection_name,10query=text_segment.embeddings_float,  # Use the embedding vector11)1213print("Text Query Results:", text_results)
```

```plaintext
1# Generate text embedding2text_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4text="A white rabbit",  # Input query5).text_embedding.segments[0]67# Perform semantic search in Qdrant8text_results = qdrant_client.query_points(9collection_name=collection_name,10query=text_segment.embeddings_float,  # Use the embedding vector11)1213print("Text Query Results:", text_results)
```

```plaintext
1# Generate audio embedding2audio_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4audio_url="https://codeskulptor-demos.commondatastorage.googleapis.com/descent/background%20music.mp3",  # Audio file URL5).audio_embedding.segments[0]67# Perform semantic search in Qdrant8audio_results = qdrant_client.query_points(9collection_name=collection_name,10query=audio_segment.embeddings_float,  # Use the embedding vector11)1213print("Audio Query Results:", audio_results)
```

```plaintext
1# Generate audio embedding2audio_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4audio_url="https://codeskulptor-demos.commondatastorage.googleapis.com/descent/background%20music.mp3",  # Audio file URL5).audio_embedding.segments[0]67# Perform semantic search in Qdrant8audio_results = qdrant_client.query_points(9collection_name=collection_name,10query=audio_segment.embeddings_float,  # Use the embedding vector11)1213print("Audio Query Results:", audio_results)
```

```plaintext
1# Generate image embedding2image_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4image_url="https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-1170x780.jpg",  # Image URL5).image_embedding.segments[0]67# Perform semantic search in Qdrant8image_results = qdrant_client.query_points(9collection_name=collection_name,10query=image_segment.embeddings_float,  # Use the embedding vector11)1213print("Image Query Results:", image_results)
```

```plaintext
1# Generate image embedding2image_segment = twelvelabs_client.embed.create(3model_name="Marengo-retrieval-2.7",4image_url="https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-1170x780.jpg",  # Image URL5).image_embedding.segments[0]67# Perform semantic search in Qdrant8image_results = qdrant_client.query_points(9collection_name=collection_name,10query=image_segment.embeddings_float,  # Use the embedding vector11)1213print("Image Query Results:", image_results)
```


---

### Snowflake - Multimodal Video Understanding {#snowflake---multimodal-video-understanding}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/snowflake-multimodal-video-understanding*

##### Oracle - Unleashing Video Intelligence

#### Code Examples

```plaintext
VECTOR
```


---

### Vespa - Multivector video retrieval {#vespa---multivector-video-retrieval}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/vespa-multivector-video-retrieval*

### Generate summaries and keywords

The code below uploads videos to an index and monitors the processing status:

Once the videos are processed, you can generate rich metadata using the /summarize and /analyze endpoints. This code creates summaries and lists of keywords for each video to enhance search capabilities:

### Create video embeddings

The code below creates multimodal embeddings for each video. These embeddings capture the temporal and contextual nuances of the video content:

See the Create video embeddings section for details.

### Create text emeddings

The code below generates an embedding for your text query:

See the Create text embeddings section for details.

### Perform hybrid searches

The code below uses Vespa’s approximate nearest neighbor (ANN) search capabilities to combine lexical search (BM25) with vector similarity ranking. The query retrieves the top hit based on hybrid ranking:

After reading this page, you have the following options:

- Customize and use the example: Use the video_search_twelvelabs_cloud notebook to understand how the integration works. You can make changes and add functionalities to suit your specific use case.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### Weaviate - Leveraging RAG for Improved Video Processing Times

#### Code Examples

```plaintext
1def on_task_update(task: EmbeddingsTask):2print(f"  Status={task.status}")34for video_url in VIDEO_URLs:5task = client.task.create(index_id=index.id, url=video_url, language="en")6status = task.wait_for_done(sleep_interval=10, callback=on_task_update)7if task.status != "ready":8raise RuntimeError(f"Indexing failed with status {task.status}")
```

```plaintext
1def on_task_update(task: EmbeddingsTask):2print(f"  Status={task.status}")34for video_url in VIDEO_URLs:5task = client.task.create(index_id=index.id, url=video_url, language="en")6status = task.wait_for_done(sleep_interval=10, callback=on_task_update)7if task.status != "ready":8raise RuntimeError(f"Indexing failed with status {task.status}")
```

```plaintext
/summarize
```

```plaintext
/analyze
```

```plaintext
1summaries = []2keywords_array = []3titles = [4"Mr. Bean the Animated Series Holiday for Teddy",5"Twas the night before Christmas",6"Hide and Seek with Giant Jenny",7]89videos = client.index.video.list(index_id)10for video in videos:11# Generate summary12res = client.generate.summarize(13video_id=video.id,14type="summary",15prompt="Generate an abstract of the video serving as metadata on the video, up to five sentences."16)17summaries.append(res.summary)1819# Generate keywords20keywords = client.generate.text(21video_id=video.id,22prompt="Based on this video, I want to generate five keywords for SEO. Provide just the keywords as a comma delimited list."23)24keywords_array.append(keywords.data)
```

```plaintext
1summaries = []2keywords_array = []3titles = [4"Mr. Bean the Animated Series Holiday for Teddy",5"Twas the night before Christmas",6"Hide and Seek with Giant Jenny",7]89videos = client.index.video.list(index_id)10for video in videos:11# Generate summary12res = client.generate.summarize(13video_id=video.id,14type="summary",15prompt="Generate an abstract of the video serving as metadata on the video, up to five sentences."16)17summaries.append(res.summary)1819# Generate keywords20keywords = client.generate.text(21video_id=video.id,22prompt="Based on this video, I want to generate five keywords for SEO. Provide just the keywords as a comma delimited list."23)24keywords_array.append(keywords.data)
```

```plaintext
1task_ids = []23for url in VIDEO_URLs:4task = client.embed.task.create(model_name="Marengo-retrieval-2.7", video_url=url)5task_ids.append(str(task.id))6status = task.wait_for_done(sleep_interval=10, callback=on_task_update)7if task.status != "ready":8raise RuntimeError(f"Embedding failed with status {task.status}")910tasks = []11for task_id in task_ids:12task = client.embed.task.retrieve(task_id)13tasks.append(task)
```

```plaintext
1task_ids = []23for url in VIDEO_URLs:4task = client.embed.task.create(model_name="Marengo-retrieval-2.7", video_url=url)5task_ids.append(str(task.id))6status = task.wait_for_done(sleep_interval=10, callback=on_task_update)7if task.status != "ready":8raise RuntimeError(f"Embedding failed with status {task.status}")910tasks = []11for task_id in task_ids:12task = client.embed.task.retrieve(task_id)13tasks.append(task)
```

```plaintext
1client = TwelveLabs(api_key=TL_API_KEY)2user_query = "Santa Claus on his sleigh"34# Generate embedding for the query5res = client.embed.create(6model_name="Marengo-retrieval-2.7",7text=user_query,8)910print("Created a text embedding")11print(f" Model: {res.model_name}")12if res.text_embedding is not None and res.text_embedding.segments is not None:13q_embedding = res.text_embedding.segments[0].embeddings_float14print(f" Embedding Dimension: {len(q_embedding)}")15print(f" Sample 5 values from array: {q_embedding[:5]}")
```

```plaintext
1client = TwelveLabs(api_key=TL_API_KEY)2user_query = "Santa Claus on his sleigh"34# Generate embedding for the query5res = client.embed.create(6model_name="Marengo-retrieval-2.7",7text=user_query,8)910print("Created a text embedding")11print(f" Model: {res.model_name}")12if res.text_embedding is not None and res.text_embedding.segments is not None:13q_embedding = res.text_embedding.segments[0].embeddings_float14print(f" Embedding Dimension: {len(q_embedding)}")15print(f" Sample 5 values from array: {q_embedding[:5]}")
```

```plaintext
1with app.syncio(connections=1) as session:2response: VespaQueryResponse = session.query(3yql="select * from videos where userQuery() OR ({targetHits:100}nearestNeighbor(embeddings,q))",4query=user_query,5ranking="hybrid",6hits=1,7body={"input.query(q)": q_embedding},8)9assert response.is_successful()1011# Print the top hit12for hit in response.hits:13print(json.dumps(hit, indent=4))1415# Get full response JSON16response.get_json()
```

```plaintext
1with app.syncio(connections=1) as session:2response: VespaQueryResponse = session.query(3yql="select * from videos where userQuery() OR ({targetHits:100}nearestNeighbor(embeddings,q))",4query=user_query,5ranking="hybrid",6hits=1,7body={"input.query(q)": q_embedding},8)9assert response.is_successful()1011# Print the top hit12for hit in response.hits:13print(json.dumps(hit, indent=4))1415# Get full response JSON16response.get_json()
```


---

### Voxel51 - Semantic video search plugin {#voxel51---semantic-video-search-plugin}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/voxel-51-semantic-video-search-plugin*

### Create an index

The plugin invokes the POST method of the /indexes endpoint to create an index and enable the Marengo video understanding engine with the engine options that the user has selected:

### Upload videos

The plugin invokes the POST method of the /tasks endpoint. Then, it monitors the indexing process using the GET method of the /tasks/{task_id} endpoint:

### Perform semantic searches

The plugin invokes the POST method of the /search endpoint to search across the sources of information that the user has selected:

After reading this page, you have several options:

- Use the plugin as-is: Inspect the source code to better understand the platform’s features and start using the plugin immediately.
- Customize and enhance the plugin: Feel free to modify the code to meet your specific requirements.
- Explore further: Try the applications built by the community or our sample applications to get more insights into the TwelveLabs Video Understanding Platform’s diverse capabilities and learn more about integrating the platform into your applications.

##### MindsDB - The TwelveLabs handler

#### Code Examples

```plaintext
POST
```

```plaintext
/indexes
```

```plaintext
1INDEX_NAME = ctx.params.get("index_name")23INDEXES_URL = f"{API_URL}/indexes"45headers = {6"x-api-key": API_KEY7}89so = []1011if ctx.params.get("visual"):12so.append("visual")13if ctx.params.get("logo"):14so.append("logo")15if ctx.params.get("text_in_video"):16so.append("text_in_video")17if ctx.params.get("conversation"):18so.append("conversation")1920data = {21"engine_id": "marengo2.7",22"index_options": so,23"index_name": INDEX_NAME,24}2526response = requests.post(INDEXES_URL, headers=headers, json=data)
```

```plaintext
1INDEX_NAME = ctx.params.get("index_name")23INDEXES_URL = f"{API_URL}/indexes"45headers = {6"x-api-key": API_KEY7}89so = []1011if ctx.params.get("visual"):12so.append("visual")13if ctx.params.get("logo"):14so.append("logo")15if ctx.params.get("text_in_video"):16so.append("text_in_video")17if ctx.params.get("conversation"):18so.append("conversation")1920data = {21"engine_id": "marengo2.7",22"index_options": so,23"index_name": INDEX_NAME,24}2526response = requests.post(INDEXES_URL, headers=headers, json=data)
```

```plaintext
POST
```

```plaintext
/tasks
```

```plaintext
GET
```

```plaintext
/tasks/{task_id}
```

```plaintext
1TASKS_URL = f"{API_URL}/tasks"23videos = target_view4for sample in videos:5if sample.metadata.duration < 4:6continue7else:8file_name = sample.filepath.split("/")[-1]9file_path = sample.filepath10file_stream = open(file_path,"rb")1112headers = {13"x-api-key": API_KEY14}1516data = {17"index_id": INDEX_ID,18"language": "en"19}2021file_param=[22("video_file", (file_name, file_stream, "application/octet-stream")),]2324response = requests.post(TASKS_URL, headers=headers, data=data, files=file_param)25TASK_ID = response.json().get("_id")26print (f"Status code: {response.status_code}")27pprint (response.json())2829TASK_STATUS_URL = f"{API_URL}/tasks/{TASK_ID}"30while True:31response = requests.get(TASK_STATUS_URL, headers=headers)32STATUS = response.json().get("status")33if STATUS == "ready":34break35time.sleep(10)3637VIDEO_ID = response.json().get('video_id')38sample["TwelveLabs " + INDEX_NAME] = VIDEO_ID39sample.save()
```

```plaintext
1TASKS_URL = f"{API_URL}/tasks"23videos = target_view4for sample in videos:5if sample.metadata.duration < 4:6continue7else:8file_name = sample.filepath.split("/")[-1]9file_path = sample.filepath10file_stream = open(file_path,"rb")1112headers = {13"x-api-key": API_KEY14}1516data = {17"index_id": INDEX_ID,18"language": "en"19}2021file_param=[22("video_file", (file_name, file_stream, "application/octet-stream")),]2324response = requests.post(TASKS_URL, headers=headers, data=data, files=file_param)25TASK_ID = response.json().get("_id")26print (f"Status code: {response.status_code}")27pprint (response.json())2829TASK_STATUS_URL = f"{API_URL}/tasks/{TASK_ID}"30while True:31response = requests.get(TASK_STATUS_URL, headers=headers)32STATUS = response.json().get("status")33if STATUS == "ready":34break35time.sleep(10)3637VIDEO_ID = response.json().get('video_id')38sample["TwelveLabs " + INDEX_NAME] = VIDEO_ID39sample.save()
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
1SEARCH_URL = f"{API_URL}/search"23headers = {4"x-api-key": API_KEY5}67so = []89if ctx.params.get("visual"):10so.append("visual")11if ctx.params.get("logo"):12so.append("logo")13if ctx.params.get("text_in_video"):14so.append("text_in_video")15if ctx.params.get("conversation"):16so.append("conversation")1718data = {19"query": prompt,20"index_id": INDEX_ID,21"search_options": so,22}2324response = requests.post(SEARCH_URL, headers=headers, json=data)25video_ids = [entry['video_id'] for entry in response.json()['data']]26print(response.json())27samples = []28view1 = target_view.select_by("TwelveLabs " + INDEX_NAME, video_ids,ordered=True)29start = [entry['start'] for entry in response.json()['data']]30end = [entry['end'] for entry in response.json()['data']]31if "results" in ctx.dataset.get_field_schema().keys():32ctx.dataset.delete_sample_field("results")3334i=035for sample in view1:36support = [int(start[i]*sample.metadata.frame_rate)+1 ,int(end[i]*sample.metadata.frame_rate)+1]37sample["results"] = fo.TemporalDetection(label=prompt, support=tuple(support))38sample.save()3940view2 = view1.to_clips("results")41ctx.trigger("set_view", {"view": view2._serialize()})4243return {}
```

```plaintext
1SEARCH_URL = f"{API_URL}/search"23headers = {4"x-api-key": API_KEY5}67so = []89if ctx.params.get("visual"):10so.append("visual")11if ctx.params.get("logo"):12so.append("logo")13if ctx.params.get("text_in_video"):14so.append("text_in_video")15if ctx.params.get("conversation"):16so.append("conversation")1718data = {19"query": prompt,20"index_id": INDEX_ID,21"search_options": so,22}2324response = requests.post(SEARCH_URL, headers=headers, json=data)25video_ids = [entry['video_id'] for entry in response.json()['data']]26print(response.json())27samples = []28view1 = target_view.select_by("TwelveLabs " + INDEX_NAME, video_ids,ordered=True)29start = [entry['start'] for entry in response.json()['data']]30end = [entry['end'] for entry in response.json()['data']]31if "results" in ctx.dataset.get_field_schema().keys():32ctx.dataset.delete_sample_field("results")3334i=035for sample in view1:36support = [int(start[i]*sample.metadata.frame_rate)+1 ,int(end[i]*sample.metadata.frame_rate)+1]37sample["results"] = fo.TemporalDetection(label=prompt, support=tuple(support))38sample.save()3940view2 = view1.to_clips("results")41ctx.trigger("set_view", {"view": view2._serialize()})4243return {}
```


---

### Weaviate - Leveraging RAG for Improved Video Processing Times {#weaviate---leveraging-rag-for-improved-video-processing-times}

*Source: https://docs.twelvelabs.io/docs/resources/partner-integrations/weaviate-leveraging-rag-for-improved-video-processing-times*

##### Chroma - Multimodal RAG: Chat with Videos


---

### Platform overview {#platform-overview}

*Source: https://docs.twelvelabs.io/docs/resources/platform-overview#queryprompt-processing-engine*

### Indexes

An index is a basic unit for organizing and storing video data consisting of video embeddings and metadata. Indexes facilitate information retrieval and processing.

### Video understanding models

A video understanding model consists of a family of deep neural networks built on top of our multimodal foundation model for video understanding, offering search and summarization capabilities. For each index, you must configure the models you want to enable. See the Video understanding models page for more details about the available models and their capabilities.

### Model options

The model options define the types of information that a specific model will process. Currently, the platform provides the following model options: visual and audio. For more details, see the Model options page.

### Query/Prompt Processing Engine

This component processes the following user inputs and returns the corresponding results to your application:

- Search queries
- Prompts for analyzing videos and generating text based on their content

##### Playground


---

### Playground {#playground}

*Source: https://docs.twelvelabs.io/docs/resources/playground*

##### Manage indexes


---

### Sample applications {#sample-applications}

*Source: https://docs.twelvelabs.io/docs/resources/sample-applications*

##### Partner integrations


---

### TwelveLabs SDKs {#twelvelabs-sdks}

*Source: https://docs.twelvelabs.io/docs/resources/twelve-labs-sd-ks*

##### Frequently asked questions


---

### Migration guide {#migration-guide}

*Source: https://docs.twelvelabs.io/v1.3/docs/resources/migration-guide*

### Global changes

### Deprecated endpoints

### Upload videos

### Manage indexes

### Manage videos

### Search

### Generate text from video

These changes add new functionality while maintaining backward compatibility.

### Upload videos

Migrating to v1.3 involves two main steps:

- Update your integration
- Update your code. Refer to the Migration Examples setion for details.

### 1. Update your integration

Choose the appropriate method based on how you interact with the TwelveLabs API:

- Official SDKs: Install version 0.4.x or later.
- HTTP client: Update your base URL.

### 2. Migration examples

Below are examples showing how to update your code for key breaking changes. Choose the examples matching your integration type.

#### Create indexes

Creating an index in version 1.3 includes the following key changes:

- Renamed parameters: The parameters that previously began with engine* have now been renamed to model*.
- Simplified modalities: The previous modalities of [visual, conversation, text_in_video, logo] have been simplified to [visual, audio].
- Marengo version update: Use “marengo2.7” instead of “marengo2.6”.

#### Perform a search request

Performing a search request includes the following key changes:

- Simplified modalities: The previous modalities of [visual, conversation, text_in_video, logo] have been simplified to [visual, audio].
- Deprecated parameter: The conversation_option parameter has been deprecated.
- Streamlined response: The metadata and modules fields in the response have been deprecated.

#### Create embeddings

Creating embeddings includes the following key changes:

- Marengo version update: Use “Marengo-retrieval-2.7” instead of “Marengo-retrieval-2.6”.
- Renamed parameter: The parameters that previously began with engine* have now been renamed to model*.

The following example creates a text embedding, but the principles demonstrated are similar for image, audio, and video embeddings:

#### Use Pegasus to classify videos

The Pegasus video understanding model offers flexible video classification through its text generation capabilities. You can use established category systems like YouTube video categories or IAB Tech Lab Content Taxonomy . You can also define custom categories for your specific needs.

The example below classifies a video based on YouTube’s video categories:

#### Detect logos

You can search for logos using text or image queries:

- Text queries: For logos that include text (example: Nike)
- Image queries: For logos without text (example: Apple’s apple symbol).

The following example searches for the Nike logo using a text query:

The following example searches for the Apple logo using an image query:

#### Search for text shown in videos

To search for text in videos, use text queries that target either on-screen text or spoken words in transcriptions rather than objects or concepts. The platform searches across both:

- Text shown on screen (such as titles, captions, or signs)
- Spoken words from audio transcriptions

Note that the platform may return both textual and visual matches. For example, searching for the word “smartphone” might return:

- Segments where “smartphone” appears as on-screen text.
- Segments where “smartphone” is spoken.
- Segments where smartphones are visible as objects.

The example below finds all the segments where the word “innovation” appears as on-screen text or as a spoken word in transcriptions:

#### Code Examples

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
engines
```

```plaintext
models
```

```plaintext
engine_name
```

```plaintext
model_name
```

```plaintext
engine_options
```

```plaintext
model_options
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation
```

```plaintext
audio
```

```plaintext
logo
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
text_in_video
```

```plaintext
/indexes
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
conversation
```

```plaintext
/search-v2
```

```plaintext
/search
```

```plaintext
/search
```

```plaintext
/classify
```

```plaintext
/engines
```

```plaintext
/engines/{engine-id}
```

```plaintext
/indexes/{index-id}/videos/{video-id}/text-in-video
```

```plaintext
/indexes/{index-id}/videos/{video-id}/logo
```

```plaintext
/indexes/{index_id}/videos/{video_id}/thumbnail
```

```plaintext
/indexes/{index-id}/videos/{video-id}/transcription
```

```plaintext
/search
```

```plaintext
/search/combined
```

```plaintext
/search
```

```plaintext
/search/combined
```

```plaintext
POST
```

```plaintext
/tasks
```

```plaintext
disable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
true
```

```plaintext
disable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
enable_video_stream
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
id
```

```plaintext
estimated_time
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}
```

```plaintext
_id
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos
```

```plaintext
metadata
```

```plaintext
user_metadata
```

```plaintext
user_metadata
```

```plaintext
metadata
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos
```

```plaintext
metadata
```

```plaintext
system_metadata
```

```plaintext
system_metadata
```

```plaintext
metadata
```

```plaintext
GET
```

```plaintext
/indexes/{index-id}/videos/{video-id}
```

```plaintext
metadata
```

```plaintext
system_metadata
```

```plaintext
system_metadata
```

```plaintext
metadata
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
conversation_option
```

```plaintext
conversation_option
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
GET
```

```plaintext
/search/{page-token}
```

```plaintext
page_info.page_expired_at
```

```plaintext
page_info.page_expires_at
```

```plaintext
page_expires_at
```

```plaintext
page_expired_at
```

```plaintext
POST
```

```plaintext
/search
```

```plaintext
GET
```

```plaintext
/search/{page-token}
```

```plaintext
metadata
```

```plaintext
modules
```

```plaintext
POST
```

```plaintext
/generate
```

```plaintext
stream
```

```plaintext
true
```

```plaintext
stream
```

```plaintext
false
```

```plaintext
POST
```

```plaintext
/tasks
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
GET
```

```plaintext
/tasks/{task-id
```

```plaintext
video_id
```

```plaintext
GET
```

```plaintext
/tasks
```

```plaintext
status
```

```plaintext
$pip3 install twelvelabs --upgrade
```

```plaintext
$pip3 install twelvelabs --upgrade
```

```plaintext
engine*
```

```plaintext
model*
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5},6{7"name": "pegasus1.2",8"options": ["visual", "audio"]9}10]11index = client.index.create(12name="<YOUR_INDEX_NAME>",13models=models,14addons=["thumbnail"] # Optional15)
```

```plaintext
1models = [2{3"name": "marengo2.7",4"options": ["visual", "audio"]5},6{7"name": "pegasus1.2",8"options": ["visual", "audio"]9}10]11index = client.index.create(12name="<YOUR_INDEX_NAME>",13models=models,14addons=["thumbnail"] # Optional15)
```

```plaintext
visual
```

```plaintext
conversation
```

```plaintext
text_in_video
```

```plaintext
logo
```

```plaintext
visual
```

```plaintext
audio
```

```plaintext
conversation_option
```

```plaintext
metadata
```

```plaintext
modules
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="<YOUR_QUERY>",4options=["visual", "audio"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="<YOUR_QUERY>",4options=["visual", "audio"]5)
```

```plaintext
engine*
```

```plaintext
model*
```

```plaintext
1res = client.embed.create(2model_name="Marengo-retrieval-2.7",3text="<YOUR_TEXT>",4)
```

```plaintext
1res = client.embed.create(2model_name="Marengo-retrieval-2.7",3text="<YOUR_TEXT>",4)
```

```plaintext
1res = client.generate.text(2video_id="<YOUR_VIDEO_ID>",3prompt="Classify this video using up to five labels from YouTube standard content categories. Provide the results in the JSON format."4)
```

```plaintext
1res = client.generate.text(2video_id="<YOUR_VIDEO_ID>",3prompt="Classify this video using up to five labels from YouTube standard content categories. Provide the results in the JSON format."4)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Nike",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Nike",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_media_type="image",4query_media_url="https://logodownload.org/wp-content/uploads/2013/12/apple-logo-16.png,5options=["visual"]6)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_media_type="image",4query_media_url="https://logodownload.org/wp-content/uploads/2013/12/apple-logo-16.png,5options=["visual"]6)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Innovation",4options=["visual"]5)
```

```plaintext
1search_results = client.search.query(2index_id="<YOUR_INDEX_ID>",3query_text="Innovation",4options=["visual"]5)
```


---

### TwelveLabs SDKs {#twelvelabs-sdks}

*Source: https://docs.twelvelabs.io/v1.3/docs/resources/twelve-labs-sd-ks*

##### Frequently asked questions


---
