# TRANSFORMERS DOCUMENTATION
Source: https://huggingface.co/docs/transformers/quicktour

Quickstart
Hugging Face
Models
Datasets
Spaces
Community
Docs
Enterprise
Pricing
Log In
Sign Up
Transformers documentation
Quickstart
Transformers
🏡 View all docs
AWS Trainium & Inferentia
Accelerate
Argilla
AutoTrain
Bitsandbytes
Chat UI
Dataset viewer
Datasets
Deploying on AWS
Diffusers
Distilabel
Evaluate
Google Cloud
Google TPUs
Gradio
Hub
Hub Python Library
Huggingface.js
Inference Endpoints (dedicated)
Inference Providers
Kernels
LeRobot
Leaderboards
Lighteval
Microsoft Azure
Optimum
PEFT
Safetensors
Sentence Transformers
TRL
Tasks
Text Embeddings Inference
Text Generation Inference
Tokenizers
Trackio
Transformers
Transformers.js
smolagents
timm
Search documentation
main
v5.0.0rc1
v4.57.3
v4.56.2
v4.55.4
v4.53.3
v4.52.3
v4.51.3
v4.50.0
v4.49.0
v4.48.2
v4.47.1
v4.46.3
v4.45.2
v4.44.2
v4.43.4
v4.42.4
v4.41.2
v4.40.2
v4.39.3
v4.38.2
v4.37.2
v4.36.1
v4.35.2
v4.34.1
v4.33.3
v4.32.1
v4.31.0
v4.30.0
v4.29.1
v4.28.1
v4.27.2
v4.26.1
v4.25.1
v4.24.0
v4.23.1
v4.22.2
v4.21.3
v4.20.1
v4.19.4
v4.18.0
v4.17.0
v4.16.2
v4.15.0
v4.14.1
v4.13.0
v4.12.5
v4.11.3
v4.10.1
v4.9.2
v4.8.2
v4.7.0
v4.6.0
v4.5.1
v4.4.2
v4.3.3
v4.2.2
v4.1.1
v4.0.1
v3.5.1
v3.4.0
v3.3.1
v3.2.0
v3.1.0
v3.0.2
v2.11.0
v2.10.0
v2.9.1
v2.8.0
v2.7.0
v2.6.0
v2.5.1
v2.4.1
v2.3.0
v2.2.2
v2.1.1
v2.0.0
v1.2.0
v1.1.0
v1.0.0
doc-builder-html
AR
DE
EN
ES
FR
HI
IT
JA
KO
PT
ZH
Get started
Transformers
Installation
Quickstart
Base classes
Inference
Training
Quantization
Export to production
Resources
Contribute
API
Join the Hugging Face community
and get access to the augmented documentation experience
Collaborate on models, datasets and Spaces
Faster examples with accelerated inference
Switch between documentation themes
Sign Up
to get started
Copy page
Quickstart
Transformers is designed to be fast and easy to use so that everyone can start learning or building with transformer models.
The number of user-facing abstractions is limited to only three classes for instantiating a model, and two APIs for inference or training. This quickstart introduces you to Transformers’ key features and shows you how to:
load a pretrained model
run inference with
Pipeline
fine-tune a model with
Trainer
Set up
To start, we recommend creating a Hugging Face
account
. An account lets you host and access version controlled models, datasets, and
Spaces
on the Hugging Face
Hub
, a collaborative platform for discovery and building.
Create a
User Access Token
and log in to your account.
notebook
CLI
Paste your User Access Token into
notebook_login
when prompted to log in.
Copied
from
huggingface_hub
import
notebook_login

notebook_login()
Install Pytorch.
Copied
!pip install torch
Then install an up-to-date version of Transformers and some additional libraries from the Hugging Face ecosystem for accessing datasets and vision models, evaluating training, and optimizing training for large models.
Copied
!pip install -U transformers datasets evaluate accelerate timm
Pretrained models
Each pretrained model inherits from three base classes.
Class
Description
PreTrainedConfig
A file that specifies a models attributes such as the number of attention heads or vocabulary size.
PreTrainedModel
A model (or architecture) defined by the model attributes from the configuration file. A pretrained model only returns the raw hidden states. For a specific task, use the appropriate model head to convert the raw hidden states into a meaningful result (for example,
LlamaModel
versus
LlamaForCausalLM
).
Preprocessor
A class for converting raw inputs (text, images, audio, multimodal) into numerical inputs to the model. For example,
PreTrainedTokenizer
converts text into tensors and
ImageProcessingMixin
converts pixels into tensors.
We recommend using the
AutoClass
API to load models and preprocessors because it automatically infers the appropriate architecture for each task and machine learning framework based on the name or path to the pretrained weights and configuration file.
Use
from_pretrained()
to load the weights and configuration file from the Hub into the model and preprocessor class.
When you load a model, configure the following parameters to ensure the model is optimally loaded.
device_map="auto"
automatically allocates the model weights to your fastest device first.
dtype="auto"
directly initializes the model weights in the data type they’re stored in, which can help avoid loading the weights twice (PyTorch loads weights in
torch.float32
by default).
Copied
from
transformers
import
AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
"meta-llama/Llama-2-7b-hf"
, dtype=
"auto"
, device_map=
"auto"
)
tokenizer = AutoTokenizer.from_pretrained(
"meta-llama/Llama-2-7b-hf"
)
Tokenize the text and return PyTorch tensors with the tokenizer. Move the model to an accelerator if it’s available to accelerate inference.
Copied
model_inputs = tokenizer([
"The secret to baking a good cake is "
], return_tensors=
"pt"
).to(model.device)
The model is now ready for inference or training.
For inference, pass the tokenized inputs to
generate()
to generate text. Decode the token ids back into text with
batch_decode()
.
Copied
generated_ids = model.generate(**model_inputs, max_length=
30
)
tokenizer.batch_decode(generated_ids)[
0
]
'<s> The secret to baking a good cake is 100% in the preparation. There are so many recipes out there,'
Skip ahead to the
Trainer
section to learn how to fine-tune a model.
Pipeline
The
Pipeline
class is the most convenient way to inference with a pretrained model. It supports many tasks such as text generation, image segmentation, automatic speech recognition, document question answering, and more.
Refer to the
Pipeline
API reference for a complete list of available tasks.
Create a
Pipeline
object and select a task. By default,
Pipeline
downloads and caches a default pretrained model for a given task. Pass the model name to the
model
parameter to choose a specific model.
text generation
image segmentation
automatic speech recognition
Use
Accelerator
to automatically detect an available accelerator for inference.
Copied
from
transformers
import
pipeline
from
accelerate
import
Accelerator

device = Accelerator().device

pipeline = pipeline(
"text-generation"
, model=
"meta-llama/Llama-2-7b-hf"
, device=device)
Prompt
Pipeline
with some initial text to generate more text.
Copied
pipeline(
"The secret to baking a good cake is "
, max_length=
50
)
[{
'generated_text'
:
'The secret to baking a good cake is 100% in the batter. The secret to a great cake is the icing.\nThis is why we’ve created the best buttercream frosting reci'
}]
Trainer
Trainer
is a complete training and evaluation loop for PyTorch models. It abstracts away a lot of the boilerplate usually involved in manually writing a training loop, so you can start training faster and focus on training design choices. You only need a model, dataset, a preprocessor, and a data collator to build batches of data from the dataset.
Use the
TrainingArguments
class to customize the training process. It provides many options for training, evaluation, and more. Experiment with training hyperparameters and features like batch size, learning rate, mixed precision, torch.compile, and more to meet your training needs. You could also use the default training parameters to quickly produce a baseline.
Load a model, tokenizer, and dataset for training.
Copied
from
transformers
import
AutoModelForSequenceClassification, AutoTokenizer
from
datasets
import
load_dataset

model = AutoModelForSequenceClassification.from_pretrained(
"distilbert/distilbert-base-uncased"
)
tokenizer = AutoTokenizer.from_pretrained(
"distilbert/distilbert-base-uncased"
)
dataset = load_dataset(
"rotten_tomatoes"
)
Create a function to tokenize the text and convert it into PyTorch tensors. Apply this function to the whole dataset with the
map
method.
Copied
def
tokenize_dataset
(
dataset
):
return
tokenizer(dataset[
"text"
])
dataset = dataset.
map
(tokenize_dataset, batched=
True
)
Load a data collator to create batches of data and pass the tokenizer to it.
Copied
from
transformers
import
DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
Next, set up
TrainingArguments
with the training features and hyperparameters.
Copied
from
transformers
import
TrainingArguments

training_args = TrainingArguments(
    output_dir=
"distilbert-rotten-tomatoes"
,
    learning_rate=
2e-5
,
    per_device_train_batch_size=
8
,
    per_device_eval_batch_size=
8
,
    num_train_epochs=
2
,
    push_to_hub=
True
,
)
Finally, pass all these separate components to
Trainer
and call
train()
to start.
Copied
from
transformers
import
Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset[
"train"
],
    eval_dataset=dataset[
"test"
],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()
Share your model and tokenizer to the Hub with
push_to_hub()
.
Copied
trainer.push_to_hub()
Congratulations, you just trained your first model with Transformers!
Next steps
Now that you have a better understanding of Transformers and what it offers, it’s time to keep exploring and learning what interests you the most.
Base classes
: Learn more about the configuration, model and processor classes. This will help you understand how to create and customize models, preprocess different types of inputs (audio, images, multimodal), and how to share your model.
Inference
: Explore the
Pipeline
further, inference and chatting with LLMs, agents, and how to optimize inference with your machine learning framework and hardware.
Training
: Study the
Trainer
in more detail, as well as distributed training and optimizing training on specific hardware.
Quantization
: Reduce memory and storage requirements with quantization and speed up inference by representing weights with fewer bits.
Resources
: Looking for end-to-end recipes for how to train and inference with a model for a specific task? Check out the task recipes!
Update
on GitHub
←
Installation
Loading models
→
Quickstart
Set up
Pretrained models
Pipeline
Trainer
Next steps
