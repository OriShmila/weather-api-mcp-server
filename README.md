# Weather API MCP Server

A comprehensive Model Context Protocol (MCP) server for weather data with bulletproof schema validation. Built with the standard MCP framework and featuring explicit tool schemas, comprehensive testing, and full input/output validation.

## 🌟 Features

### Weather Tools
- **Current weather conditions** - Real-time weather with optional air quality
- **Weather forecasts** - 1-14 day forecasts with alerts and air quality
- **Weather alerts** - Severe weather warnings and advisories  
- **Air quality information** - Pollution levels and health indices
- **Astronomy data** - Sunrise, sunset, moon phases, and solar/lunar positions
- **Location search** - Find and identify locations by name, coordinates, postal codes, or airport codes
- **Timezone information** - Time zone data for any location
- **Sports events** - Weather for sporting events (football, cricket, golf)

### Advanced Features
- **🔍 Comprehensive Schema Validation** - Full JSON Schema validation for inputs and outputs
- **📋 Explicit Tool Definitions** - All tools defined in `tools.json` with complete schemas
- **🧪 Extensive Testing** - 45+ test cases covering all tools and edge cases
- **⚡ High Performance** - 100% success rate with optimized API calls
- **🛡️ Error Handling** - Robust validation and meaningful error messages
- **📊 Real-time Validation** - Input parameters validated before API calls

## 📋 Available Tools

| Tool | Description | Required Parameters | Optional Parameters |
|------|-------------|-------------------|-------------------|
| `get_current_weather` | Current weather conditions | `query` | `include_air_quality` |
| `get_weather_forecast` | Weather forecasts (1-14 days) | `query` | `days`, `include_air_quality`, `include_alerts` |
| `get_weather_alerts` | Weather warnings and alerts | `query` | - |
| `get_weather_airquality` | Air quality measurements | `query` | - |
| `get_astronomy_data` | Astronomy and solar/lunar data | `query`, `date` | - |
| `search_locations` | Search and find locations (no weather data) | `query` | - |
| `get_timezone` | Timezone information | `query` | - |
| `get_weather_for_sport_event` | Sports event weather | `query` | - |

> **Note:** `get_weather_history` is available but requires a premium WeatherAPI subscription.

## 🛠️ Requirements

 - **Python 3.11+**
- **[uv](https://github.com/astral-sh/uv)** package manager
- **[WeatherAPI](https://www.weatherapi.com/)** API key (free tier available)

## 🚀 Installation

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather-api-mcp-server.git
   cd weather-api-mcp-server
   ```

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Set up your API key:**
   ```bash
   # Create .env file
   echo "WEATHER_API_KEY=your_api_key_here" > .env
   ```

4. **Get your WeatherAPI key:**
   - Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
   - Copy your API key to the `.env` file

## 📖 Usage

### Running the Server

#### Option 1 (recommended): Run via uvx console script

Add to your MCP client's settings (example for Claude Desktop):

```json
{
  "mcpServers": {
    "weatherAPI": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/OriShmila/weather-api-mcp-server",
        "weather-api-mcp-server"
      ],
      "env": {
        "WEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### Option 2: Local run (repo checkout)

```bash
# Start the MCP server from a local checkout
uv run python main.py
```

The server runs as an MCP server using stdin/stdout communication protocol.

### Testing the Server

```bash
# Run comprehensive test suite (45+ tests)
uv run python test_server.py
```

**Expected output:**
```
🌤️  Weather API MCP Server Test Suite
==================================================
✅ Loaded 9 tool schemas
✅ Mapped 9 tool functions
🔍 Validating schema structure...
✅ All schemas have valid structure
✅ All schemas have corresponding functions
✅ Loaded 5 schema definitions for $ref resolution

🧪 Running Tool Tests with Schema Validation
--------------------------------------------------
🚀 Running 45 test cases with full schema validation...

...

==================================================
🧪 TEST SUMMARY
==================================================
Total Tests: 45
✅ Passed: 45
❌ Failed: 0
📊 Success Rate: 100.0%
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `WEATHER_API_KEY` | Your WeatherAPI.com API key | Yes |

### Tool Schemas

All tool schemas are defined in `tools.json` with:
- **Input validation** - Parameter types, constraints, patterns
- **Output validation** - Response structure and data types  
- **$ref definitions** - Reusable schema components
- **Error handling** - Comprehensive validation rules

## 📊 Schema Validation

This server features comprehensive JSON Schema validation:

### Input Validation
- ✅ **Parameter types** (string, integer, boolean)
- ✅ **Required fields** validation
- ✅ **Pattern matching** (date formats, etc.)
- ✅ **Range constraints** (min/max values)
- ✅ **Enum validation** 

### Output Validation  
- ✅ **Response structure** validation
- ✅ **Field type checking**
- ✅ **Required properties** validation
- ✅ **$ref resolution** for reusable definitions
- ✅ **Nested object validation**

### Example: Date Validation
```bash
# ✅ Valid date format
"date": "2024-12-25"

# ❌ Invalid date format (caught by schema)
"date": "2024/12/25"  # Error: does not match '^\\d{4}-\\d{2}-\\d{2}$'
```

## 🧪 Testing

The server includes comprehensive testing:

- **45 test cases** covering all tools
- **5 tests per tool** with different scenarios  
- **Error case validation** for edge cases
- **Real API call testing** with live validation
- **Schema validation testing** for inputs/outputs
- **Performance monitoring** with response times

### Test Categories

1. **Positive Tests** - Valid inputs and expected outputs
2. **Negative Tests** - Invalid inputs and error handling
3. **Edge Cases** - Boundary conditions and limits
4. **Schema Tests** - Input/output validation
5. **Performance Tests** - Response time monitoring

## 🔗 MCP Client Integration

### Claude Desktop Configuration

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "weatherAPI": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/OriShmila/weather-api-mcp-server",
        "weather-api-mcp-server"
      ],
      "env": {
        "WEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Other MCP Clients

The server implements the standard MCP protocol and works with any MCP-compatible client:

- **stdin/stdout communication**
- **JSON-RPC 2.0 protocol**
- **Tool listing and execution**
- **Comprehensive error handling**

## 📁 Project Structure

```
weather-api-mcp-server/
├── main.py              # MCP server implementation
├── tools.json           # Tool schemas and definitions
├── test_server.py       # Comprehensive test suite
├── test_cases.json      # Test cases (45+ scenarios)
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables
└── README.md            # This file
```

## 🎯 Query Examples

### Location Flexibility
```python
# City names
"query": "London"
"query": "New York"

# Coordinates  
"query": "40.7128,-74.0060"

# Postal codes
"query": "10001"

# Airport codes
"query": "LAX"
```

### Weather Forecasts
```python
# Basic forecast
{
  "query": "Paris",
  "days": 3
}

# Advanced forecast with air quality and alerts
{
  "query": "Miami", 
  "days": 7,
  "include_air_quality": true,
  "include_alerts": true
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run python test_server.py`
5. Submit a pull request

## 🙏 Acknowledgments

- [WeatherAPI.com](https://www.weatherapi.com/) for providing comprehensive weather data
- [MCP Framework](https://github.com/modelcontextprotocol) for the protocol specification
- [UV Package Manager](https://github.com/astral-sh/uv) for fast dependency management