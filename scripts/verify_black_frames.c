/* Decode and compare every RGB pixel without writing terabytes through a pipe. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/imgutils.h>
#include <libswscale/swscale.h>

static void fail(const char *message) {
    fprintf(stderr, "%s\n", message);
    exit(1);
}

static long frames = 0;
static long title_frames;
static int title_present = 0;
static struct SwsContext *scaler;
static uint8_t *rgb[4];
static int stride[4];
static uint8_t *black;
static const int width = 1280, height = 720;

static void receive(AVCodecContext *decoder, AVFrame *frame) {
    int result;
    while ((result = avcodec_receive_frame(decoder, frame)) >= 0) {
        if (frame->width != width || frame->height != height ||
            frame->format != AV_PIX_FMT_YUV420P ||
            frame->color_range != AVCOL_RANGE_MPEG)
            fail("Unexpected decoded video format or range");
        if (sws_scale(scaler, (const uint8_t *const *)frame->data,
                      frame->linesize, 0, height, rgb, stride) != height)
            fail("RGB conversion failed");
        int is_black = memcmp(rgb[0], black, (size_t)width * height * 3) == 0;
        if (frames == 0) title_present = !is_black;
        if (frames >= title_frames && !is_black) {
            fprintf(stderr, "Nonblack RGB pixel in frame %ld\n", frames);
            exit(1);
        }
        frames++;
        av_frame_unref(frame);
    }
    if (result != AVERROR(EAGAIN) && result != AVERROR_EOF)
        fail("Video decode failed");
}

int main(int argc, char **argv) {
    if (argc != 4) fail("Usage: verify-black-frames VIDEO EXPECTED_FRAMES TITLE_FRAMES");
    long expected = strtol(argv[2], NULL, 10);
    title_frames = strtol(argv[3], NULL, 10);
    if (expected <= title_frames || title_frames < 1) fail("Invalid frame counts");
    AVFormatContext *format = NULL;
    if (avformat_open_input(&format, argv[1], NULL, NULL) < 0 ||
        avformat_find_stream_info(format, NULL) < 0) fail("Cannot open video");
    const AVCodec *codec = NULL;
    int stream = av_find_best_stream(format, AVMEDIA_TYPE_VIDEO, -1, -1, &codec, 0);
    if (stream < 0) fail("No video stream");
    AVCodecContext *decoder = avcodec_alloc_context3(codec);
    if (!decoder || avcodec_parameters_to_context(decoder, format->streams[stream]->codecpar) < 0)
        fail("Cannot configure decoder");
    decoder->thread_count = 1;
    decoder->err_recognition = AV_EF_EXPLODE;
    if (avcodec_open2(decoder, codec, NULL) < 0) fail("Cannot open decoder");
    scaler = sws_getContext(width, height, AV_PIX_FMT_YUV420P,
                            width, height, AV_PIX_FMT_RGB24, SWS_BICUBIC,
                            NULL, NULL, NULL);
    if (!scaler || av_image_alloc(rgb, stride, width, height, AV_PIX_FMT_RGB24, 1) < 0)
        fail("Cannot allocate RGB conversion");
    const int *matrix = sws_getCoefficients(SWS_CS_ITU709);
    if (sws_setColorspaceDetails(scaler, matrix, 0, matrix, 1, 0, 1<<16, 1<<16) < 0)
        fail("Cannot set video color conversion");
    black = calloc((size_t)width * height * 3, 1);
    AVPacket *packet = av_packet_alloc();
    AVFrame *frame = av_frame_alloc();
    if (!black || !packet || !frame) fail("Allocation failed");
    int result;
    while ((result = av_read_frame(format, packet)) >= 0) {
        if (packet->stream_index == stream) {
            if (avcodec_send_packet(decoder, packet) < 0) fail("Packet decode failed");
            receive(decoder, frame);
        }
        av_packet_unref(packet);
    }
    if (result != AVERROR_EOF) fail("Video read failed");
    if (avcodec_send_packet(decoder, NULL) < 0) fail("Cannot flush decoder");
    receive(decoder, frame);
    if (frames != expected || !title_present) fail("Wrong frame count or missing title");
    printf("{\"decoded_rgb_frames\":%ld,\"black_frame_count\":%ld,\"title_present\":true}\n",
           frames, frames-title_frames);
    av_packet_free(&packet);
    av_frame_free(&frame);
    avcodec_free_context(&decoder);
    avformat_close_input(&format);
    sws_freeContext(scaler);
    av_freep(&rgb[0]);
    free(black);
    return 0;
}
