# TypeArm
The TypeFly system aims to generate robot task plans using a large language model (LLM) and our custom programming language `MiniSpec`. Link to [full paper](https://drive.google.com/file/d/1COrozqEIk6v8DLxI3vCgoSUEWpnsc2mu/view) and [webpage](https://typefly.github.io/).

Also, check out the demo video for TypeArm here: [Demo 1: "Go to the bottle, then zoom in” followed by “zoom out”](https://youtu.be/MBxjSt7ASBc?si=PO9ab6eddttJimjn), [Demo 2: "Go to the ball, stay there for 4 seconds, then go to the bottle"](https://youtu.be/pMSC09IX0vk?si=yzu7VLx1hTH8m-jV).

## Hardware Requirement
To use TypeArm, you will need a compatible robot arm, such as the Neuromeka Indy7 Pro (with IndyEye). Since Neuromeka arm requires your device to connect to its wifi and TypeFly requires Internet connection, you need to have both wifi adapter and ethernet adapter to run TypeFly.

## Software Requirement
Make sure you have the necessary packages installed for TypeArm. If you're using a virtual environment, activate it before installing the packages with `pip3 install neuromeka`.

## OPENAI API KEY Requirement
TypeFly use GPT-4 API as the remote LLM planner, please make sure you have set the `OPENAI_API_KEY` environment variable.

## Vision Encoder
TypeFly uses YOLOv8 to generate the scene description. We provide the implementation of gRPC YOLO service and a optional http router to serve as a scheduler when working with multiple drones. We recommand using [docker](https://docs.docker.com/engine/install/ubuntu/) to run the YOLO and router. To deploy the YOLO servive with docker, please install the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), then run the following command:
```bash
make SERVICE=yolo build
```
Optional: To deploy the router, please run the following command:
```bash
make SERVICE=router build
```

## TypeFly Web UI
To play with the TypeFly web UI, please run the following command:
```bash
make typefly
```
This will start the web UI at `http://localhost:50001` with your default camera (please make sure your device has a camera) and a virtual drone wrapper. You should be able to see the image capture window displayed with YOLO detection results. You can test the planning ability of TypeFly by typing in the chat box. 

To work with a virtual or other type of robot, please replace the `--arm` flag in `Makefile`.

Here we assume your YOLO and router are deployed on the same machine running the TypeFly webui, if not, please define the environment variables `VISION_SERVICE_IP`, which is the IP address where you deploy your YOLO (or router) service, before running the webui.

## Task Execution
Here are some examples of task descriptions, the `[Q]` prefix indicates TypeFly will output an answer to the question:
- `Is there something to drink on the table? If so, go to it and zoom in.`
- `Go to the bottle, pause for 3 seconds, and go to the ball.`
- `[Q] Tell me how many items you can see on the table?`
