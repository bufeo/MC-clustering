#include <Python.h>
#include <stdlib.h>

/*TODOS:

 * the new way of calling DBSCAN crashed -> is it the values or the way I call it?
 -> try a python example

 * building the data creates problem. It is the PyList_Append function -> but WHY??

 * when things work: clean up and find meaningful names for parameters! 

 * shift as much functionality as possible to python code
 */
int main()
{


  //--------------------------------------------------
  // SET PARAMETERS
  //--------------------------------------------------
  int min_samples = 10;
  double eps = 5.;

  //--------------------------------------------------
  // INITIALIZE DATA: toy data
  //--------------------------------------------------
  int i, j, k;
  int data_length = 2000;
  int data [data_length][3];

  for(i=0; i<10; i++){
    for(j=0; j<10; j++){
      for(k=0; k<10;k++){

	data[k + 10*i + 100*j][0] = 10+i;
	data[k + 10*i + 100*j][1] = 10+j;
	data[k + 10*i + 100*j][2] = 10+k;

	data[1000 +k + 10*i + 100*j][0] = 30+i;
	data[1000 +k + 10*i + 100*j][1] = 30+j;
	data[1000 +k + 10*i + 100*j][2] = 30+k;

      }
    }
  }

  //  printf("%d, %d, %d\n", data[1999][0], data[1999][1], data[1999][2]);
  //--------------------------------------------------
  // SET UP AND RUN PYTHON
  //--------------------------------------------------

  //start Python
  Py_Initialize();

  // build python arguments for clustering parameters
  PyObject *pArgCon = NULL;
  pArgCon = Py_BuildValue("{s:i:s:f}","min_samples",min_samples,"eps",eps);

  PyObject* pData = NULL;

  //build python arguments for data

  const Py_ssize_t tuple_length = 3;
  pData = PyList_New(0);

  for(i = 0; i < data_length; i++) {
    PyObject *the_tuple = PyTuple_New(tuple_length);

    for(Py_ssize_t p = 0; p < tuple_length; p++) {
      PyObject *the_object = Py_BuildValue("i",data[i][p]);
      PyTuple_SET_ITEM(the_tuple, j, the_object);
      Py_DECREF(the_object);
    }
    PyList_Append(pData, the_tuple);
    //if(PyList_Append(pData, the_tuple) == -1) {
      //return 1;
      //}
    Py_DECREF(the_tuple);
  }
 

  pData = Py_BuildValue("{}");

  if(pArgCon && pData)
    {
      printf("Python Arguments succesfully initialized\n");
    }
  else
    {
      printf("error initializing python arguments");
      return 1;
    }

  printf("some shit\n");
  
  PyObject *pName = PyString_FromString((char*)"sklearn.cluster");
  if(pName) printf("some shit\n");

  PyObject *pModule = PyImport_Import(pName);
  if(pModule) printf("some shit\n");

  
  // pDict is a borrowed reference
  PyObject *pDict = PyModule_GetDict(pModule);
  if(pDict) printf("someshit\n");
 
  //get an object from the dictionary
  pName =  PyString_FromString((char*)"DBSCAN");
  PyObject *pDBSCAN =  PyDict_GetItem(pDict, pName); 
  PyObject *pCalled = NULL;
  

  printf("ckeck\n");
  if(PyCallable_Check(pDBSCAN) && pArgCon)
    {
      printf("it's a callable\n");
      pCalled = PyObject_Call(pDBSCAN, pData, pArgCon);
    }
   

  if(PyInstance_Check(pCalled))
    {
      printf("it's a instane\n");
    }
  else if(PyCallable_Check(pCalled))
    {
      printf("it's again a callable\n");
    }
  else if(PyClass_Check(pCalled))
    {
      printf("it's a class\n");
    }
  else
    {
      printf("it's somethin mysterious new!\n");
    }

  printf("\ncalled and it didn't crash...\n\n");


  return 0;
  
  
   
   //testin arguments
   /*
   if(!pArgCon)
     {
       printf("Arguments not properly initialized\n");
       return 1;
     }
   else
     {
       printf("Argument initialization worked\n");
     }
   */

   //testing type
   /*
  if (PyClass_Check(pDBSCAN))
     {
       printf("it's a class\n");
     }
   else if(PyCallable_Check(pDBSCAN))
     {
       printf("it's a callable\n");
       // try to call the thing...
     }
   else
     {
       printf("try further\n");  
     }
   */

   // Clean up
   //make sure to get rid of all PyObject*
   //Py_DECREF(pModule);
   //Py_DECREF(pFunc);
   //Py_DECREF(pDict);

   // Finish the Python Interpreter
   Py_Finalize();
  return 0;

}
