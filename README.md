# Ultrasonic sensor Height Classification using analog waveform features

This repository implements a **signal processing + machine learning pipeline for ultrasonic sensing**, focusing on **Height Classification** of localized objects using analog waveform features.

> This work represent my research dissertation thesis project:  
> **"Ultrasonic sensor Height Classification using analog waveform features"**   
> *(Faculty of Electronics, Telecommunications and Information Technology, Cluj-Napoca 2025).*  

## 🚀Project Overview

Ultrasonic sensors provide reliable range information for object detection in parking scenarios. Height classification is a paradigm where sinGle or multiple ultra sonic sensors are used in order to estimate the height of identified objects in the scene with the scope of determining if the object are traversable or not by the car.

In order to do that echo detection and feature extraction are essential for building robust algorithms for identifying the type of object. For this are applying both signal processing techniques and machine learning algorithms to effectively extract and process information from the analog signal, which encapsulates the information of ultra sound waves reflected by objects situated in the surrounding of the vehicle.

This project develops both online and post-processing methods for ultrasonic echo detection and integrates them into a classification pipeline. The extracted features are used to train machine learning models for height classification tasks on a rp2350 micro-controller.

## 🎯Table of Contents

- [Ultrasonic sensor Height Classification using analog waveform features](#ultrasonic-sensor-height-classification-using-analog-waveform-features)
  - [🚀Project Overview](#project-overview)
  - [🎯Table of Contents](#table-of-contents)
  - [⚡Microcontroller](#microcontroller)
  - [📂Dataset](#dataset)
  - [🔊Signal Processing](#signal-processing)
  - [🤖Machine Learning](#machine-learning)
  - [🔧Building the project](#building-the-project)
  - [📚Bibliography](#bibliography)

## ⚡Microcontroller
  * Low power, low cost compared to GPU/CPU inference.

  * Suitable for real-time, embedded ultrasonic sensing (e.g., in cars).

  * Constraints: limited RAM (tens–hundreds of KB), flash storage, and no floating-point hardware on some MCUs.

  * RP2350 (Raspberry Pi RP2040 family).

  * Dual ARM Cortex-M33+ (150 MHz)

  * 264 KB SRAM

  * FPU enables fast IRR and FIR filters

## 📂Dataset

## 🔊Signal Processing

## 🤖Machine Learning

## 🔧Building the project

## 📚Bibliography