# target executable name
TARGET = PA01

# Compiler
CC=g++

# Compiler Flags
CXXFLAGS = -g -Wall -std=c++11

# Source files
SOURCES = driver.cpp PA01.cpp

# header file dependencies
HEADERS =

# Object files
OBJECTS = $(SOURCES:.cpp=.o)

#default target
all: $(TARGET)

# link everything together
$(TARGET):	$(OBJECTS)
				$(CC) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

$(OBJECTS):	$(SOURCES) $(HEADERS)
				$(CC) $(CXXFLAGS) -c $(SOURCES)

# Clean target
clean:
		rm $(TARGET) $(OBJECTS)