<!DOCTYPEhtml>
 <html lang="en-US">
  <body>

<h1>Morgan State Computer Science Medical Annotation Research</h1>

<h2>Design Princples</h2>
<ol>
	<li>OOP is used rather than Procedural Programming because it is faster
	to make a large data structure global to the instance of the class rather
	than pass by value.</li>
	<li id="DP2">The system is multi-threaded because each step of getting and formatting
	data does not need to wait for the previous step to finish. This will
	esure that large data sets get process as quickly as possible.</li>
</ol>

<h2>External Libraries Used</h2>
<ol>
	<li>The CV2 library is used to crop and save images that have unions.</li>
	<li>The WGET library is used to download all the images from the internet.</li>
	<li>The Pandas library is used to read and write data to and from CSV files.</li>
</ol>

<h2>Native Modules Used</h2>
<ol>
	<li>The OS module is used to check if the unfiltered CSV file exist and create needed directories.</li>
	<li>The Threading module is used to create multi-threaded work loads. See <a href="#DP2">Design Princple #2</a>.</li>
</ol>

<h2>Flow of Control</h2>
<ol>
	<li>Check if the user generated results file exists.<br />
	<img src="" alt="Does CSV Exist?" /></li>
	<li>Start threads to download images and get user generated response data.<br />
	<img src="../MSU-CS/code/codeImages/threading1.png" alt="Threading #1" /></li>
	<li>Downloading images thread uses the wget library is used to download all the images in the results CSV files.<br />
	<img scr="../MSU-CS/code/codeImages/downloadImages.png" alt="Download Images" /></li>
	<li>The get responses thead get all the selected keywords and store them in a file<br />
	<img src="../MSU-CS/code/codeImages/getResponses.png" alt="Get responses" /></li>
	<li>The main thread will create an instance of FindUnion and generate meta data constants.</li><br />
	<img src="../MSU-CS/code/codeImages/metaDataConsts.png" alt="Meta Data Constants" />
	<li>The cropping algorithm takes each users cropping value and puts them into 1D arrays to be used in the crop method.</li><br />
	<img src="../MSU-CS/code/codeImages/croppingAlg.png" alt="Cropping Algorithm" />
	<li>Crop each image according to the values stored in 1D arrays</li><br />
	<img src="../MSU-CS/code/codeImages/crop.png" alt="Crop Method" />
</ol>

 </body>
</html>
