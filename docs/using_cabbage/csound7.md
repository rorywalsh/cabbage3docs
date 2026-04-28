---
title: Csound 7
description: Csound 7 in Cabbage
---

Cabbage 3 is built on Csound 7, the latest major release of the Csound audio programming language. Csound 7 is not a drop-in replacement for Csound 6 — it introduces breaking changes — but the improvements it brings make it a much stronger foundation for building audio plugins and instruments. This page highlights the Csound 7 features most relevant to Cabbage users.

## Explicit Variable Types

Csound 7 introduces explicit type declarations, moving away from the traditional requirement of prefixing variables with i, k, or a to define their rate. You can now use descriptive, custom names for your variables, provided you declare their type upon initialization:

```csound
count:i = 0
freq:k  = 440
arr:k[] init 1, 2, 3, 4

print count

```

For Cabbage instrument authors, this makes code considerably easier to read and maintain, especially in larger instruments or when sharing code with other users. 

## User-Defined Structs

Csound 7 adds support for user-defined struct types, allowing related data to be grouped together in a meaningful way:

```csound
struct MyType val0:i, val1:i

instr 1
  testVal:MyType init 8, 88
  print(testVal.val0)
  print(testVal.val1)
endin

```

For Cabbage users building complex instruments structs provide a clean way to organise state that previously required verbose naming conventions or unwieldy arrays. The following is an example of a struct that can be used to represent the two outputs of a Cabbage button:

```
struct CabbageButton trig:k, val:k

instr Effect

  mute:CabbageButton init 0, 0
  compress:CabbageButton

  mute.val, mute.trig = cabbageGetValue("muteWidget)
  compress.val, compress.trig = cabbageGetValue("compressWidget)
  (...)

endin
```

## Improved User-Defined Opcodes (UDOs) with Pass-by-Reference

In Csound 7, UDOs support pass-by-reference for array and struct arguments. Previously, passing an array into a UDO made a copy of the entire array on every k-cycle, which was costly and made in-place processing awkward. To avail of this new pass-by-reference you need to use the updated UDO syntax, shown below:

```csound
opcode MyCustomOp(inval:i):(i)
  xout(inval+1)
endop
```

This is especially useful in Cabbage instruments that use UDOs as reusable DSP modules (filters, envelope stages, effects chains). It reduces memory overhead, makes the intent of the code clearer, and enables patterns that simply weren't practical before.

## Oversampling

Csound 7 provides built-in oversampling support, allowing sections of your signal chain to run at a higher sample rate than the host. This directly addresses two common problems in audio plugin development:

- **Aliasing in non-linear processing** — distortion, waveshaping, and saturation all generate harmonics that can fold back into the audible range at standard sample rates. Running the non-linear stage at 2× or 4× eliminates this.
- **High-frequency accuracy in modulation and synthesis** — oscillators and filters behave more accurately at higher internal rates, which is audible on material with significant high-frequency content. 

The following User-Defined Opcode (UDO) performs 8x oversampling, significantly reducing the risk of aliasing caused by wavetable inaccuracies.

```csound
opcode oversampleOscil, a,kki
    amp:k, freq:k, table:i xin
    oversample(8, 4)
    sig:a = oscili(amp, freq, table)
    filteredSig:a = tone(sig, 22000)
    xout filteredSig
endop
```

Note that this UDO utilises traditional syntax. In this context, Csound employs a pass-by-copy mechanism; however, since we are only passing a few scalar arguments, the performance overhead is negligible and not a cause for concern.

For Cabbage users building guitar effects, synthesizers, or any instrument involving distortion or aggressive filtering, oversampling is a straightforward way to achieve more professional-sounding results without changing the host's sample rate setting.

## Parallel Opcode Execution

Csound 7 introduces the ability to instantiate and run arrays of opcodes in parallel. This addresses a fundamental limitation in Csound: the inability to use standard loops for multi-signal processing.

### The Problem: Statefulness
Most opcodes in Csound are stateful; they rely on internal memory (like filter coefficients or delay buffers) that must persist across k-cycles. If you try to "re-use" a single opcode inside a while loop to process an array of signals, the internal state is overwritten every iteration, resulting in noise or errors.

In Csound 6, the most effective, albeit a little inaccessible way of having a bank of opcodes was through a recursive UDO. In Csound 7, the new `Opcode[]` handles this by managing a dedicated internal state for every individual instance in the opcode array.

```csound
instr FilterBank
   ; 1. Create an array of frequencies for our filters
   freq:i[] fillarray p5*0.75, p5, p5*1.333, p5*1.666

   ; 2. The 'create' opcode constructs a bank of 'reson' filters.
   ; The number of filters is determined by the length of the frequency array.
   obj:Opcode[] create reson, lenarray(freq)

   src:a rand linenr(p4, 0.1, 0.1, 0.01)

   ; 3. The 'run' opcode processes the entire filter bank.
   ; It takes the opcode array and an argument list matching the 'reson' signature.
   sig:a[] run obj, src, freq, freq/p6, 2

   out sumarray(sig) / lenarray(sig)
endin
```

By replacing complex recursive logic with a single Opcode[] declaration and the run command, Csound 7 provides a much more accessible path for Cabbage developers to build high-density synthesis engines and parallel processing chains.

---

These features collectively make Csound 7 a significantly more capable host environment for Cabbage than Csound 6 was. The language changes in particular — explicit types, structs, and improved UDOs — reward writing clean, well-structured instrument code, and that structure maps well onto the way Cabbage manages UI state and plugin parameters.

