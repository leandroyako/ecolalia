(
s.options.numBuffers_(2097152);
s.boot;

SynthDef.new(\playbuf, {
	arg amp=1, out=0, pos=0, buf, rate=1, da=2;
	var sig, env;
	env = Env.asr(0.01, BufDur.kr(buf) - 0.02, 0.01).kr(doneAction:da);
	sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf) * rate);
	sig = sig * env;
	sig = Pan2.ar(sig, pos) * amp;
	Out.ar(out, sig);
}).writeDefFile;

~wavs_dir = "~/sc/nosotros_clean";

~soundfiles = SoundFile.collectIntoBuffers(~wavs_dir+/+"*");
~soundfiles.sort({|a, b| a.duration > b.duration})
)

z = Array.iota(~soundfiles.size,15);

~groups = ~soundfiles.reshapeLike(z)


(
~score = Score.new;

~soundfiles.do({|buf|
	~score.add([0, buf.allocReadMsg(buf.path)]);
});

~pattern = Pbind(
	\instrument, \playbuf,
	\buf, Pseq(~groups),
	\dur, 1.2,
	\amp, 0.1,
);

~pattern = ~pattern.asScore(300);

~pattern.score.do{|e| ~score.add(e)};

// Destination path and file name
~outFile = thisProcess.nowExecutingPath.asPathName.pathOnly ++ "durations_nrt.wav";

// Render the score as wav file
~score.recordNRT(
	outputFilePath: ~outFile.asAbsolutePath,
	headerFormat: "wav",
	sampleFormat: "float",
	options: ServerOptions.new.numOutputBusChannels_(2).numBuffers_(2097152).maxNodes_(32768).memSize_(2 ** 21),
	action: { "done".postln }
);
)
