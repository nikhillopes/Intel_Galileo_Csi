# Intel_Galileo_Csi
Resources for collecting channel state information of IEEE 802.11n networks on an Intel Galileo Board
 
The pre-built image is availble in this repository in the image folder.

To build the image yourself follow the following instructions:

1. To modify the kernel to enable CSI collection please use the patch file in this repo.

2. To enable this modification into the Yocto layer please follow instructions available <a href="https://downloadmirror.intel.com/23197/eng/quark-x1000-bsp-build-sw-rel-user-guide..pdf">here</a>.
 
3. Instructions to build the Yocto Linux Image are <a href="https://software.intel.com/en-us/blogs/2015/03/04/creating-a-yocto-image-for-the-intel-galileo-board-using-split-layers">here</a>

4. To write the image file use <a href="https://software.intel.com/en-us/programming-blank-sd-card-with-yocto-linux-image-linux">these</a> instructions. 

More resources and pre-compiled binaries of frequently used system utilities are available <a href="http://iotdk.intel.com/" >here</a>
