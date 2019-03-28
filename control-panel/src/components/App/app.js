export default {
  name: 'App',

  data() {
    return {
      iconSize: 14,
    };
  },

  computed: {
    activeName() {
      return this.$route.name;
    },
  },

  methods: {
    goToPage(name) {
      this.$router.push({ name });
    },
  },
};
