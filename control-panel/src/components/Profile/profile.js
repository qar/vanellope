import apis from '@/utils/api';

export default {
  name: 'Profile',

  data() {
    return {
      profile: {},
    };
  },

  mounted() {
    apis.getUserProfile().then((res) => {
      this.profile = res.data;
    });
  },

  methods: {
    save() {
      apis.updateUserProfile(this.profile);
    },

    sendVerifyLinkToEmail(email) {
      apis.sendVerifyLinkToEmail(email);
    },
  },
};

