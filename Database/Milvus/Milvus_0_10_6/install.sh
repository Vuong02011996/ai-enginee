sudo docker run -d --restart=always --name milvus_gpu_0.10.6 --gpus all -p 8010:19530 -p 8011:19121 -v /home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Milvus/Milvus_0_10_6/milvus_volumes/db:/var/lib/milvus/db -v /home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Milvus/Milvus_0_10_6/milvus_volumes/conf:/var/lib/milvus/conf -v /home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Milvus/Milvus_0_10_6/milvus_volumes/logs:/var/lib/milvus/logs -v /home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Milvus/Milvus_0_10_6/milvus_volumes/wal:/var/lib/milvus/wal milvusdb/milvus:0.10.6-gpu-d022221-64ddc2
