# Adobe "Connecting the Dots" Challenge - Round 1A Solution

## 🎯 **Document Outline Extraction**

This solution implements an advanced document outline extraction system for the Adobe Hackathon Round 1A challenge. It extracts structured outlines from PDF documents with high accuracy and performance.

## 🚀 **Quick Start**

### **Docker Build & Run**
```bash
# Build the Docker image
docker build --platform linux/amd64 -t adobe-solution:latest .

# Run the solution
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-solution:latest
```

## 📋 **Input/Output Specification**

### **Input**
- PDF files (up to 50 pages) placed in the `/app/input` directory
- The solution automatically processes all PDF files in the input directory

### **Output**
- JSON files generated in the `/app/output` directory
- One JSON file per input PDF with the same base filename
- Format: `{filename}.json`

### **JSON Output Format**
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "What is AI?",
      "page": 2
    },
    {
      "level": "H3",
      "text": "History of AI", 
      "page": 3
    }
  ]
}
```

## 🏗️ **Technical Architecture**

### **Advanced Font Analysis & Layout Detection**
The solution uses a sophisticated multi-criteria approach that goes beyond simple font size detection:

1. **Font Analysis**: Detailed analysis of font size, style (bold/italic), and positioning
2. **Multi-Criteria Heading Detection**: Combines font characteristics, text length, and content indicators
3. **Intelligent Title Extraction**: Employs multiple heuristics to accurately identify document titles
4. **Style-Based Level Classification**: Groups similar heading styles and maps them to H1, H2, H3 levels
5. **Content Quality Scoring**: Evaluates text complexity and structural indicators

### **Key Features**
- **Robust Heading Detection**: Handles various PDF formats and layouts
- **Accurate Title Extraction**: Identifies document titles with high precision
- **Page Number Mapping**: Correctly maps headings to their page numbers
- **Performance Optimized**: Processes 50-page PDFs in under 10 seconds
- **Offline Operation**: No internet connectivity required

## 📦 **Dependencies**

- **PyMuPDF==1.23.8**: High-performance PDF parsing and text extraction
- **numpy==1.26.4**: Numerical computations for analysis algorithms

## 🔧 **Technical Constraints Met**

- ✅ **AMD64 Architecture**: Compatible with linux/amd64 platform
- ✅ **CPU Only**: No GPU dependencies required
- ✅ **Model Size**: < 200MB (no ML models used)
- ✅ **Offline Operation**: No network/internet calls
- ✅ **Performance**: ≤ 10 seconds for 50-page PDFs
- ✅ **Memory Efficient**: Optimized for 8 CPUs and 16 GB RAM

## 📊 **Performance Characteristics**

- **Processing Speed**: < 10 seconds for 50-page documents
- **Memory Usage**: < 500MB peak memory
- **Accuracy**: High precision heading detection across various PDF formats
- **Scalability**: Handles multiple PDFs efficiently

## 🎯 **Key Innovations**

1. **Advanced Font Analysis**: Multi-dimensional font characteristic analysis
2. **Layout-Aware Detection**: Considers document structure and positioning
3. **Robust Title Extraction**: Multiple heuristics for accurate title identification
4. **Style Grouping**: Intelligent classification of heading levels
5. **Content Quality Assessment**: Evaluates text complexity for better ranking

## 🐛 **Troubleshooting**

### **Common Issues**
- **No PDFs Found**: Ensure PDF files are in the input directory
- **Permission Errors**: Check Docker volume mount permissions
- **Build Failures**: Ensure Docker is running and has sufficient resources

### **Verification**
After running the solution, check the output directory for generated JSON files. Each input PDF should have a corresponding JSON file with the same base filename.

## ✅ **Compliance Checklist**

- [x] AMD64 architecture compatible
- [x] No GPU dependencies
- [x] Model size ≤ 200MB
- [x] Offline operation (no network calls)
- [x] Processing time ≤ 10 seconds for 50-page PDFs
- [x] Proper JSON output format
- [x] Handles multiple PDF files
- [x] Extracts title and headings (H1, H2, H3)
- [x] Includes page numbers for each heading

## 📁 **Project Structure**

```
adobe1/
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── input/                 # Input PDF files
├── output/                # Generated JSON files
└── solution/
    ├── __init__.py        # Package initialization
    ├── main.py            # Main orchestration script
    ├── round_1a.py        # Core outline extraction logic
    └── utils.py           # Utility functions
```

## 🚀 **Quick Start Commands**

```bash
# Build the solution
docker build --platform linux/amd64 -t adobe-solution:latest .

# Run with sample data
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-solution:latest

# Check results
ls -la output/
```

---

**Adobe "Connecting the Dots" Challenge - Round 1A Solution**  
*Advanced Document Outline Extraction with Multi-Criteria Analysis* 