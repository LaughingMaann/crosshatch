using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.CV.CvEnum;
using System;
using IronPython.Hosting;
using System.Drawing.Imaging;
using System.Drawing;


namespace CrossHatch
{
    class Program
    {
        static void Main(string[] args)
        {
            /*
            http://www.emgu.com/wiki/index.php/Working_with_Images
            "Unlike the Image<,> class, where you will need to pre-allocate memory with the correct size before passing it as an IOutputArray, 
            when an empty Mat is passed as an IOutputArray, Open CV will automatically allocate memory for the Mat. 
            You can also load an image from file using the CvInvoke.Imread function:"
            */
            Mat imgMat = CvInvoke.Imread("C:\\Users\\ester\\Documents\\sample.png", Emgu.CV.CvEnum.ImreadModes.AnyColor);  //

            /*
            "Accessing the pixels from Mat: Unlike the Image<,> class, where memory are pre-allocated and fixed, 
            the memory of Mat can be automatically re-allocated by Open CV function calls. 
            We cannot pre-allocate managed memory and assume the same memory are used through the life time of the Mat object. 
            As a result, Mat class do not contains a Data property like the Image<,> class, 
            where the pixels can be access through a managed array. To access the data of the Mat, there are a few possible choices."
            */
            Image<Bgr, Byte> imgPls = imgMat.ToImage<Bgr, Byte>();

            /*
            The pixel data can then be accessed using the Image<,>.Data property.
            You can also convert the Mat to an Matrix<> object. Assuming the Mat contains 8-bit data,
            */
            //Matrix<Byte> matrix = new Matrix<Byte>(645, 480, 3);  // why does imgMat.Rows and imgMat.Cols ==0?
            Matrix<Byte> matrix = new Matrix<Byte>(645, 480, 3);  // why does imgMat.Rows and imgMat.Cols ==0?

            //int a = imgPls.Data[0,4,1]; // why doesnt this work? System.IndexOutOfRangeException: 'Index was outside the bounds of the array.'
            //Console.WriteLine(a);

            imgMat.CopyTo(matrix);

            int rowsLen = 645;
            int colLen = 1440;
            //Matrix<Byte> unflatMat = new Matrix<Byte>(645, 480, 3);
            Image<Bgr, Byte> unflatImg = new Image<Bgr, byte>(645, 480, new Bgr(255, 0, 0));
            Bgr color;
            for (int row = 0; row < rowsLen; row++)
            {
                for (int col = 0; col < colLen; col += 3)
                {


                    int b = matrix[row, col];
                    int g = matrix[row, col + 1];
                    int r = matrix[row, col + 2];



                    unflatImg[row, col / 3] = new Bgr(b, g, r);
                }

            }



            Console.WriteLine("pls work");
            var matt = Python.CreateEngine();
            //var searchPaths = engine.GetSearchPaths();
            //searchPath.engine.
            //matt.ExecuteFile("C:\\Users\\estepark\\Documents\\python.py");

            //var mainfile = @"C:\Users\estepark\Documents"
            //var calibrationDBResult = TrueTest.APIResultEnum.Success;

            String win1 = "Test Window"; //The name of the window
            CvInvoke.NamedWindow(win1); //Create the window using the specific name
            Mat img = new Mat(200, 400, DepthType.Cv8U, 3); //Create a 3 channel image of 400x200, Mat(Int32, Int32, DepthType, Int32) 
            img.SetTo(new Bgr(255, 0, 0).MCvScalar); // set it to Blue color


            CvInvoke.PutText(
               imgPls,
               "Hello, matt",
               new System.Drawing.Point(10, 80),
               FontFace.HersheyComplex,
               1.0,
               new Bgr(0, 255, 0).MCvScalar);


            CvInvoke.Imshow(win1, unflatImg); //Show the image
            CvInvoke.WaitKey(0);  //Wait for the key pressing event
            CvInvoke.DestroyWindow(win1); //Destroy the window if key is pressed


        }
    }
}