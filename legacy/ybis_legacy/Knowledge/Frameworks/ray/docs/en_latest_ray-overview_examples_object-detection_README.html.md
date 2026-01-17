Scalable video processing — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Scalable video processing[#](#scalable-video-processing "Link to this heading")

This tutorial builds an end-to-end face mask detection pipeline that leverages distributed fine-tuning, large-scale batch inference, video analytics, and scalable serving:

[1.object\_detection\_train.ipynb](1.object_detection_train.html)  
Fine-tune a pre-trained Faster R-CNN model on a face mask dataset in Pascal Visual Object Classes (VOC) format using Ray Train. Parse XML annotations with Ray Data, retrieve images from S3, run a distributed training loop, checkpoint the model, and visualize inference results.  
![Object Detection Training Pipeline](https://face-masks-data.s3.us-east-2.amazonaws.com/tutorial-diagrams/train_object_detection.png)

[2.object\_detection\_batch\_inference\_eval.ipynb](2.object_detection_batch_inference_eval.html)  
Load a fine-tuned model from S3 into Anyscale cluster storage, perform GPU-accelerated batch inference on a test set with Ray Data, and calculate object detection metrics (mAP, IoU, recall) using TorchMetrics for comprehensive model evaluation.  
![Metrics Calculation Pipeline](https://face-masks-data.s3.us-east-2.amazonaws.com/tutorial-diagrams/batch_inference_metrics_calculation.png)

[3.video\_processing\_batch\_inference.ipynb](3.video_processing_batch_inference.html)  
Demonstrate a real-world video analytics workflow: read a video from S3, split it into frames, apply the detection model in parallel using Ray Data batch inference, draw bounding boxes and labels on each frame, and regenerate an annotated video for downstream consumption.  
![Video Processing Pipeline](https://face-masks-data.s3.us-east-2.amazonaws.com/tutorial-diagrams/video_processing.png)

[4.object\_detection\_serve.ipynb](4.object_detection_serve.html)  
Deploy the trained Faster R-CNN mask detector as a production-ready microservice using Ray Serve and FastAPI. Set up ingress, configure autoscaling and fractional GPU allocation, test the HTTP endpoint, and manage the service lifecycle both locally and through Anyscale Services.

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/examples/object-detection/README.ipynb)