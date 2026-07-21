# QW-007 Decisions

Open decisions:

1. Safetensors plus native model construction, ONNX, or another first runtime?
2. Which architectures, dtypes, devices, and operator sets are supported?
3. How are tensor channels, action remapping, masks, and value perspective
   validated before inference?
4. What numeric tolerance and deterministic fixture positions define parity?
5. Which layer owns runtime capability negotiation and error taxonomy?
