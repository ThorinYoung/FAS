

# FAS

### Quick start

1. cuda 10.x is recommended, while cuda 11.x / 12.x have not been tested for stylegan2

2. refer to env.yaml to create the environment or use this command below:

   ```  conda env create -n fas -f env.yaml
   
   ```

   if any problem occurred, please install specific packages manually, then run

   ``` conda activate fas
   
   ```

3. get checkpoints:
https://pan.quark.cn/s/350c14d48e34
   
   put them all in ./checkpoints
   
4. run the main.py 

   ``` python main.py
   
   ```

   you can get the main window as below:

 <img src="./example/1.png" alt="Description of your image">

### Example

Here are some examples: 

<div style="display: flex;">   
   <video width="256" height="256" controls>     <source src="./res/res/model_256.mp4" type="video/mp4">     Your browser does not support the video tag.   </video>      <video width="256" height="256" controls>     <source src="./res/res/res1.mp4" type="video/mp4">     Your browser does not support the video tag.   </video> 
   <video width="256" height="256" controls>     <source src="./res/res/res2.mp4" type="video/mp4">     Your browser does not support the video tag.   </video> </div>

<div style="display: flex;">
  <div style="flex: 1; text-align: center;">
    source
  </div>
  <div style="flex: 1; text-align: center;">
    result1
  </div>
  <div style="flex: 1; text-align: center;">
    +smile
  </div>
</div>
<div style="display: flex;">   
   <video width="256" height="256" controls>     <source src="./res/res/t1.mp4" type="video/mp4">     Your browser does not support the video tag.   </video>      <video width="256" height="256" controls>     <source src="./res/res/t2.mp4" type="video/mp4">     Your browser does not support the video tag.   </video> 
   <video width="256" height="256" controls>     <source src="./res/res/t3.mp4" type="video/mp4">     Your browser does not support the video tag.   </video> </div>

<div style="display: flex;">
  <div style="flex: 1; text-align: center;">
    result2
  </div>
  <div style="flex: 1; text-align: center;">
    -age
  </div>
  <div style="flex: 1; text-align: center;">
    +glass
  </div>
</div>

Examples with UI:

<img src="./example/2.gif">
<img src="./example/3.gif">

### Contributor

Gratitude to Senior Song Jiapeng for his invaluable assistance! Acknowledgments to the contributors of https://github.com/a312863063/generators-with-stylegan2 Special thanks to the contributors of https://github.com/AliaksandrSiarohin/first-order-model

### License

The project is licensed under the [Apache License 2.0] - Please refer to the [LICENSE] file for detailed information.