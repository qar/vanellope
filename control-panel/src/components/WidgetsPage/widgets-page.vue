<template>
  <div>
    <Row>
      <Col>
        <Card :bordered="false" dis-hover>
            <p slot="title">Year Progress</p>
            <Progress :stroke-width="10" :percent="yearProgress"></Progress>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'WidgetsPage',

  computed: {

    // Year progress based on UTC time
    yearProgress() {
      const currentYear = new Date().getUTCFullYear();
      const yearBeginAt = Date.UTC(currentYear, 0 /* month is ZERO-based */, 1, 0, 0, 0, 0);
      const yearEndAt = Date.UTC(currentYear + 1, 0 /* month is ZERO-based */, 1, 0, 0, 0, 0);
      const currentMoment = Date.now();
      const percentage = (currentMoment - yearBeginAt) / (yearEndAt - yearBeginAt);
      return Math.round(percentage * 100);
    },
  },
};
</script>
