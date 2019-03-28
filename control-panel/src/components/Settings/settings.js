import apis from '@/utils/api';

export default {
  name: 'Settings',

  data() {
    return {
      settings: {},
    };
  },

  mounted() {
    apis.getSettings().then((res) => {
      this.settings = res.configs;
    });
  },

  methods: {
    save() {
      apis.updateSettings(this.settings);
    },
  },
};

