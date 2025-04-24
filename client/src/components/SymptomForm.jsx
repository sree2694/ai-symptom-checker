// src/components/SymptomForm.jsx
import React, { useState } from "react";
import { TextField, Button, Box, Typography, Chip } from "@mui/material";
import axios from "axios";

const SymptomForm = () => {
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [symptomInput, setSymptomInput] = useState("");
  const [symptoms, setSymptoms] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddSymptom = () => {
    if (symptomInput && !symptoms.includes(symptomInput)) {
      setSymptoms([...symptoms, symptomInput]);
      setSymptomInput("");
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/api/check-symptoms", {
        age: parseInt(age),
        gender,
        symptoms
      });
      setResult(res.data);
    } catch (err) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 4, maxWidth: 600, mx: "auto" }}>
      <Typography variant="h5" gutterBottom>AI Symptom Checker</Typography>
      <TextField label="Age" type="number" fullWidth margin="normal" value={age} onChange={(e) => setAge(e.target.value)} />
      <TextField label="Gender" fullWidth margin="normal" value={gender} onChange={(e) => setGender(e.target.value)} />
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
          <Chip key={index} label={sym} onDelete={() => setSymptoms(symptoms.filter(s => s !== sym))} sx={{ m: 0.5 }} />
        ))}
      </Box>
      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Submit"}
      </Button>

      {result && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">AI Response:</Typography>
          {result.error ? (
            <Typography color="error">{result.error}</Typography>
          ) : (
            <ul>
              {result.conditions?.map((c, i) => (
                <li key={i}>
                  <strong>{c.name}</strong> ({c.probability}): {c.suggestion}
                </li>
              ))}
            </ul>
          )}
        </Box>
      )}
    </Box>
  );
};

export default SymptomForm;
