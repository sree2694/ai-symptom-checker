import React, { useState } from "react";
import {
  TextField,
  Button,
  Box,
  Typography,
  Chip,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  CircularProgress
} from "@mui/material";
import axios from "axios";

const SymptomForm = () => {
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [symptomInput, setSymptomInput] = useState("");
  const [symptoms, setSymptoms] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("cohere"); // default to Cohere AI

  const handleAddSymptom = () => {
    if (symptomInput && !symptoms.includes(symptomInput.toLowerCase())) {
      setSymptoms([...symptoms, symptomInput.toLowerCase()]);
      setSymptomInput("");
    }
  };

  const handleSubmit = async () => {
    if (!age || !gender || symptoms.length === 0) {
      alert("Please fill out all fields.");
      return;
    }

    setLoading(true);
    const payload = {
      age: parseInt(age),
      gender,
      symptoms,
    };
    const url =
      model === "cohere"
        ? "http://localhost:8000/api/check-symptoms"
        : "http://localhost:8000/api/predict-disease"; // Use appropriate endpoint based on model

    console.log("Sending request with payload:", payload);

    try {
      const res = await axios.post(url, payload);
      setResult(res.data);
    } catch (err) {
      console.error("Error submitting symptoms:", err);
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 4, maxWidth: 600, mx: "auto" }}>
      <Typography variant="h4" gutterBottom>
        MedAssist AI – Symptom Checker
      </Typography>

      <TextField
        label="Age"
        type="number"
        fullWidth
        margin="normal"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />

      <TextField
        select
        label="Gender"
        fullWidth
        margin="normal"
        value={gender}
        onChange={(e) => setGender(e.target.value)}
      >
        <MenuItem value="">Select</MenuItem>
        <MenuItem value="male">Male</MenuItem>
        <MenuItem value="female">Female</MenuItem>
        <MenuItem value="other">Other</MenuItem>
      </TextField>

      <FormControl fullWidth margin="normal">
        <InputLabel id="model-select-label">Prediction Model</InputLabel>
        <Select
          labelId="model-select-label"
          value={model}
          label="Prediction Model"
          onChange={(e) => setModel(e.target.value)}
        >
          <MenuItem value="cohere">Cohere AI</MenuItem>
          <MenuItem value="ml">Traditional ML Model</MenuItem>
        </Select>
      </FormControl>

      <TextField
        label="Add Symptom"
        fullWidth
        margin="normal"
        value={symptomInput}
        onChange={(e) => setSymptomInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAddSymptom()}
      />
      <Box sx={{ mb: 2 }}>
        {symptoms.map((sym, index) => (
          <Chip
            key={index}
            label={sym}
            onDelete={() => setSymptoms(symptoms.filter((s) => s !== sym))}
            sx={{ m: 0.5 }}
          />
        ))}
      </Box>

      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Submit"}
      </Button>

      {result && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            AI Response:
          </Typography>

          {result.error ? (
            <Typography color="error">{result.error}</Typography>
          ) : (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                {result.result || result.predicted_disease}
              </Typography>
            </Box>
          )}
        </Box>
      )}
    </Box>
  );
};

export default SymptomForm;
