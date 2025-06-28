# Project Directory Structure

## Overview
This document provides a comprehensive guide to the project's directory structure and important files.

## Root Directory
- `readme/` - Contains documentation images and resources
- `wildfire_1/` - Main project source code directory
- `README.md` - Main project documentation with setup instructions and overview
- `READMEADD.md` - Additional documentation
- `READMEWCS.MD` - Documentation for Web Coverage Service (WCS) components
- `READMEWFS.md` - Documentation for Web Feature Service (WFS) components
- `pyproject.toml` - Python project configuration file

## Key Documentation Files

### README.md
The primary documentation file containing:
- Project description
- Installation instructions
- Technical assets and URLs
- Usage guidelines
- Features overview
- Data sources
- Troubleshooting guide
- Cost information
- Contact details

### READMEWCS.MD
Detailed documentation about the Web Coverage Service (WCS) implementation, including:
- WCS layer specifications
- Raster data handling
- Integration details

### READMEWFS.md
Documentation focused on Web Feature Service (WFS) components:
- WFS layer specifications
- Vector data processing
- Service integration details

### READMEADD.md
Supplementary documentation with additional project information.

## Important Directories

### wildfire_1/

The main project source code directory containing:
#### app/
- API implementations /api/routes.py
- Queries required for frontend /services
- - Database modules

#### streamlit_app/
- Application source code /pages
- API client side code /api_client.py

#### wdfis_layer_extract/
- Processing scripts
- Database loading scripts
- Examples of data and visual representation

### readme/
Storage for documentation resources:
- Images
- Diagrams
- Screenshots
- Other documentation assets

## Configuration Files

### pyproject.toml
Project configuration file specifying:
- Project metadata
- Dependencies
- Build settings
- Development tools configuration

## Getting Started
1. Start with `README.md` for project overview and setup instructions
2. Refer to specific documentation files (READMEWCS.MD, READMEWFS.md) for detailed component information
3. Source code can be found in the `wildfire_1/` directory
4. Test implementations are in the `Test/` directory