-- Drop the database if it exists
DROP DATABASE IF EXISTS fitnessplanner;

-- DATABASE CHECK
-- This is used to see if the Database exists on the local computer
-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS fitnessplanner;

-- Switch to the goengine databaselog
USE fitnessplanner;
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Weight FLOAT,
    Height FLOAT,
    MuscleMass FLOAT,
    FitnessGoal VARCHAR(255),
    Preferences VARCHAR(255)
);
DELIMITER //

CREATE PROCEDURE inputMetrics(IN _UserID INT, IN _Name VARCHAR(255), IN _Weight FLOAT, IN _Height FLOAT, IN _MuscleMass FLOAT, IN _FitnessGoal VARCHAR(255), IN _Preferences VARCHAR(255))
BEGIN
    INSERT INTO Users(UserID, Name, Weight, Height, MuscleMass, FitnessGoal, Preferences) 
    VALUES (_UserID, _Name, _Weight, _Height, _MuscleMass, _FitnessGoal, _Preferences);
END //
CREATE PROCEDURE setPreferences(IN _UserID INT, IN _Preferences VARCHAR(255))
BEGIN
    UPDATE Users
    SET Preferences = _Preferences
    WHERE UserID = _UserID;
END //
CREATE PROCEDURE viewRecommendations(IN _UserID INT)
BEGIN
    -- This procedure would be more complex in a real-world scenario,
    -- involving joining tables and perhaps sophisticated algorithms.
    -- For simplicity, it just retrieves basic user data here.
    SELECT * FROM Users WHERE UserID = _UserID;
END //

CREATE TABLE Meals (
    MealID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Calories INT,
    Protein FLOAT,
    Carbs FLOAT,
    Fats FLOAT,
    Allergens VARCHAR(255),
    Type VARCHAR(255)
);
CREATE FUNCTION getNutritionalInfo(_MealID INT) RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE _info VARCHAR(255);
    SELECT CONCAT(Name, ' - Calories: ', Calories, ', Protein: ', Protein, ', Carbs: ', Carbs, ', Fats: ', Fats) INTO _info
    FROM Meals
    WHERE MealID = _MealID;
    RETURN _info;
END;


CREATE TABLE Exercises (
    ExerciseID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Difficulty VARCHAR(50),
    TargetMuscleGroup VARCHAR(255),
    CaloricExpenditure INT
);

CREATE FUNCTION getExerciseDetails(_ExerciseID INT) RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE _details VARCHAR(255);
    SELECT CONCAT(Name, ' - Difficulty: ', Difficulty, ', Target Muscle Group: ', TargetMuscleGroup, ', Caloric Expenditure: ', CaloricExpenditure) INTO _details
    FROM Exercises
    WHERE ExerciseID = _ExerciseID;
    RETURN _details;
END //

CREATE TABLE RecommendationLogs (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    RecommendationType VARCHAR(50), -- 'Meal' or 'Exercise'
    RecommendationID INT, -- MealID or ExerciseID
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE PROCEDURE generateMealPlan(IN _UserID INT)
BEGIN
    DECLARE _MealID INT;
    
    -- Example logic to select a MealID based on user preferences
    SELECT MealID INTO _MealID FROM Meals 
    WHERE Calories < 500 LIMIT 1; -- Simplified condition

    INSERT INTO RecommendationLogs(UserID, RecommendationType, RecommendationID) 
    VALUES (_UserID, 'Meal', _MealID);
END //


CREATE PROCEDURE suggestExercises(IN _UserID INT)
BEGIN
    DECLARE _ExerciseID INT;
    
    -- Example logic to select an ExerciseID based on user fitness goal
    SELECT ExerciseID INTO _ExerciseID FROM Exercises 
    WHERE Difficulty = 'Easy' LIMIT 1; -- Simplified condition

    INSERT INTO RecommendationLogs(UserID, RecommendationType, RecommendationID) 
    VALUES (_UserID, 'Exercise', _ExerciseID);
END //

CREATE TABLE NLPLogs (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Query VARCHAR(255),
    Response VARCHAR(255),
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE PROCEDURE processFeedback(IN _UserID INT, IN _Feedback VARCHAR(255))
BEGIN
    INSERT INTO NLPLogs(UserID, Query, Response) 
    VALUES (_UserID, _Feedback, 'Feedback received. Thank you!');
END //

CREATE FUNCTION answerQuery(_Query VARCHAR(255)) RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE _Response VARCHAR(255);
    
    -- Example response generation logic
    SET _Response = 'Thank you for your query. We will get back to you soon.';

    -- Log the query and response
    INSERT INTO NLPLogs(UserID, Query, Response) 
    VALUES (NULL, _Query, _Response); -- Assuming UserID is NULL for general queries

    RETURN _Response;
END //


