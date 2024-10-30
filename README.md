# VBT WhatsApp Training Bot

A WhatsApp bot that automatically processes and stores Velocity Based Training (VBT) data through WhatsApp Business API, making training data collection and analysis effortless.

## What is Velocity Based Training (VBT)?

Velocity Based Training is a method that uses movement speed to optimize resistance training. By measuring the speed of exercise execution, athletes and trainers can:

1. **Autoregulate Training Load**: Rather than using fixed percentages of 1RM (one-rep maximum), VBT allows for daily load adjustment based on your actual performance capacity.

2. **Objective Performance Tracking**: Movement velocity provides immediate, objective feedback about:
   - Fatigue levels
   - Readiness to train
   - True intensity of the exercise

3. **Enhanced Precision**: VBT helps determine:
   - When to increase/decrease weight
   - When to end a set (velocity loss)
   - Optimal loads for different training goals

### Why VBT?

Traditional percentage-based training has limitations:
- 1RM can fluctuate daily
- Doesn't account for fatigue/readiness
- Less precise for performance optimization

VBT addresses these issues by providing:
- Real-time performance data
- Objective measures of intensity
- Better autoregulation
- More precise training zones

There is a linear relationship of load (with respect to 1RM) and velocity. One can use linear regression to estimate the velocity for a given load. With this, you can also create a velocity-load profile which can help quantify the volume and intensity of training sessions much more accurately.
## Project Context

### The Problem
While VBT offers significant advantages, it comes with practical challenges:
1. Data collection is time-consuming
2. Manual analysis is tedious
3. Real-time adjustments require quick data processing
4. Tracking progress over time needs organized data storage

### The Solution
This bot automates the VBT workflow:
1. Send CSV data from your VBT sensor via WhatsApp
2. Bot processes and stores data automatically
3. Get immediate feedback and analysis
4. Track progress effortlessly

## MVP Features

1. **Data Collection**
   - Automatic processing of VBT sensor CSV data
   - Real-time storage in database during training
   - Interactive WhatsApp list messages for options

2. **Training Analysis**
   - View previous training data
   - Compare current vs past performance
   - Calculate velocity profiles for exercises

3. **Core Functionality**
   - WhatsApp webhook processing
   - State-based user interaction
   - Message handling system
   - Database integration


### Data Flow
1. User sends VBT data via WhatsApp
2. Webhook processes incoming message
3. Data is validated and processed
4. Results stored in database
5. User receives confirmation/analysis

## Future Roadmap

### Phase 1: Enhanced VBT Features
- Automatic velocity profile creation
- Performance trending
- Fatigue detection
- Load recommendations

### Phase 2: Expanded Functionality
- Voice message input for rep logging
- Natural language processing
- Possibility of tracking your food too
- General workout tracking
- Progress photos

### Phase 3: AI Integration
- Training recommendations
- Performance analysis
- Personalized feedback

## Development Status
Currently in MVP development:
- [x] Whatsapp Webhook validation with Pydantic
- [x] Simple state machine to handle bot states
- [x] Data storage implementation
- [x] Message handling system
- [ ] Refactoring of code following SOLID principles
- [ ] Testing 
- [ ] Complete analysis features
- [ ] Velocity profile automation

## Contributing
Currently in early development. Contact for contribution guidelines.

## Why This Project?

This project was born from personal experience with VBT training. While the technology offers incredible benefits for training optimization, the practical implementation often becomes a barrier. By automating the data collection and analysis through a familiar platform (WhatsApp), we remove this barrier and make VBT more accessible.

Starting with a focused MVP for VBT users, the project aims to eventually expand into a comprehensive training companion that can benefit all gym-goers, whether they use VBT or not.