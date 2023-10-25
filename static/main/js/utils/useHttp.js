export const useHttp = async (url = "", params = {}) => {
  try {
    fetch(`/packages/filter/?query=${queryStr}`)
      .then((response) => response.text())
      .then((data) => {
        return data;
      });
  } catch (err) {
    return err;
  }
};
